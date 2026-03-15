"""
OAuth 2.0 provider for single-user MCP server with Streamable HTTP transport.

Uses HMAC-signed tokens so access/refresh tokens survive server restarts.
Only auth codes and pending sessions are in-memory (short-lived).
"""

import base64
import contextlib
import hashlib
import hmac
import json
import logging
import secrets
import time
from collections.abc import AsyncIterator
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from mcp.server.lowlevel.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from starlette.routing import Route

logger = logging.getLogger(__name__)


class SimpleOAuthProvider:
    """OAuth 2.0 provider for single-user MCP server.

    Uses HMAC-signed tokens so access/refresh tokens survive server restarts.
    Only auth codes and pending sessions are in-memory (short-lived).
    """

    def __init__(self, password: str):
        self.password = password
        self.signing_key = password
        self.clients: Dict[str, Dict[str, Any]] = {}
        self.auth_codes: Dict[str, Dict[str, Any]] = {}
        self.pending_auth: Dict[str, Dict[str, Any]] = {}

    def _sign_token(self, payload: Dict[str, Any]) -> str:
        payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        payload_b64 = (
            base64.urlsafe_b64encode(payload_json.encode()).decode().rstrip("=")
        )
        sig = hmac.new(
            self.signing_key.encode(), payload_b64.encode(), hashlib.sha256
        ).hexdigest()
        return f"{payload_b64}.{sig}"

    def _verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload_b64, sig = token.rsplit(".", 1)
            expected_sig = hmac.new(
                self.signing_key.encode(), payload_b64.encode(), hashlib.sha256
            ).hexdigest()
            if not hmac.compare_digest(sig, expected_sig):
                return None
            padding = 4 - len(payload_b64) % 4
            if padding != 4:
                payload_b64 += "=" * padding
            payload = json.loads(base64.urlsafe_b64decode(payload_b64))
            if payload.get("exp", 0) < time.time():
                return None
            return payload
        except Exception:
            return None

    def register_client(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        client_id = secrets.token_urlsafe(16)
        client_secret = secrets.token_urlsafe(32)
        client = {
            **metadata,
            "client_id": client_id,
            "client_secret": client_secret,
            "client_id_issued_at": int(time.time()),
        }
        self.clients[client_id] = client
        return client

    def start_authorize(
        self,
        client_id: str,
        code_challenge: str,
        redirect_uri: str,
        state: Optional[str],
        scopes: List[str],
    ) -> str:
        session_id = secrets.token_urlsafe(32)
        self.pending_auth[session_id] = {
            "client_id": client_id,
            "code_challenge": code_challenge,
            "redirect_uri": redirect_uri,
            "state": state,
            "scopes": scopes,
        }
        return session_id

    def complete_authorize(self, session_id: str) -> Optional[tuple]:
        pending = self.pending_auth.pop(session_id, None)
        if not pending:
            return None
        code = secrets.token_urlsafe(32)
        self.auth_codes[code] = {
            **pending,
            "expires_at": time.time() + 300,
        }
        return code, pending["redirect_uri"], pending["state"]

    def exchange_code(
        self, code: str, client_id: str, code_verifier: str, redirect_uri: str
    ) -> tuple:
        auth_code = self.auth_codes.pop(code, None)
        if not auth_code:
            return None, "invalid_grant"
        if auth_code["expires_at"] < time.time():
            return None, "invalid_grant"
        if auth_code["client_id"] != client_id:
            return None, "invalid_grant"
        if auth_code["redirect_uri"] != redirect_uri:
            return None, "invalid_grant"
        # Verify PKCE (S256)
        expected = (
            base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode()).digest()
            )
            .rstrip(b"=")
            .decode()
        )
        if expected != auth_code["code_challenge"]:
            return None, "invalid_grant"
        return self._issue_tokens(client_id, auth_code["scopes"]), None

    def refresh(self, refresh_token_str: str, client_id: str) -> tuple:
        payload = self._verify_token(refresh_token_str)
        if not payload:
            return None, "invalid_grant"
        if payload.get("type") != "refresh":
            return None, "invalid_grant"
        return self._issue_tokens(client_id, payload.get("scopes", [])), None

    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        payload = self._verify_token(token)
        if not payload:
            return None
        if payload.get("type") != "access":
            return None
        return payload

    def _issue_tokens(self, client_id: str, scopes: List[str]) -> Dict[str, Any]:
        access_payload = {
            "type": "access",
            "client_id": client_id,
            "scopes": scopes,
            "exp": int(time.time()) + 86400,
        }
        refresh_payload = {
            "type": "refresh",
            "client_id": client_id,
            "scopes": scopes,
            "exp": int(time.time()) + 86400 * 30,
        }
        result: Dict[str, Any] = {
            "access_token": self._sign_token(access_payload),
            "token_type": "bearer",
            "expires_in": 86400,
            "refresh_token": self._sign_token(refresh_payload),
        }
        if scopes:
            result["scope"] = " ".join(scopes)
        return result


LOGIN_PAGE_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Trello MCP - Authorize</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 400px; margin: 80px auto; padding: 0 20px; }}
        h2 {{ color: #333; }}
        input[type="password"] {{ width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }}
        button {{ background: #0079bf; color: white; border: none; padding: 10px 24px; border-radius: 4px; cursor: pointer; font-size: 16px; }}
        button:hover {{ background: #026aa7; }}
        .error {{ color: #c00; }}
    </style>
</head>
<body>
    <h2>Authorize MCP Access</h2>
    <p>Enter your server password to grant access to your Trello data.</p>
    {error}
    <form method="POST" action="/login">
        <input type="hidden" name="session" value="{session_id}">
        <input type="password" name="password" placeholder="Server password" required autofocus>
        <button type="submit">Authorize</button>
    </form>
</body>
</html>"""


def create_http_app(mcp_server: Server, auth_token: str) -> Starlette:
    """Create a Starlette app with OAuth 2.0 authentication for remote MCP access.

    Args:
        mcp_server: The low-level MCP Server instance (e.g. from FastMCP._mcp_server).
        auth_token: The password/token used for the OAuth login flow.
    """
    oauth = SimpleOAuthProvider(auth_token)
    session_manager = StreamableHTTPSessionManager(app=mcp_server)

    async def handle_oauth_metadata(request: Request) -> Response:
        server_url = str(request.base_url).rstrip("/")
        return JSONResponse(
            {
                "issuer": server_url,
                "authorization_endpoint": f"{server_url}/authorize",
                "token_endpoint": f"{server_url}/token",
                "registration_endpoint": f"{server_url}/register",
                "response_types_supported": ["code"],
                "grant_types_supported": ["authorization_code", "refresh_token"],
                "token_endpoint_auth_methods_supported": [
                    "client_secret_post",
                    "none",
                ],
                "code_challenge_methods_supported": ["S256"],
            }
        )

    async def handle_protected_resource_metadata(request: Request) -> Response:
        server_url = str(request.base_url).rstrip("/")
        return JSONResponse(
            {
                "resource": server_url,
                "authorization_servers": [server_url],
                "bearer_methods_supported": ["header"],
            }
        )

    async def handle_register(request: Request) -> Response:
        if request.method == "GET":
            return JSONResponse(
                {
                    "registration_endpoint": f"{str(request.base_url).rstrip('/')}/register",
                    "registration_endpoint_auth_methods_supported": [],
                }
            )
        body = await request.json()
        client = oauth.register_client(body)
        return JSONResponse(client, status_code=201)

    async def handle_authorize(request: Request) -> Response:
        client_id = request.query_params.get("client_id", "")
        if not client_id or client_id not in oauth.clients:
            return JSONResponse({"error": "invalid_client"}, status_code=400)
        session_id = oauth.start_authorize(
            client_id=client_id,
            code_challenge=request.query_params.get("code_challenge", ""),
            redirect_uri=request.query_params.get("redirect_uri", ""),
            state=request.query_params.get("state"),
            scopes=(
                request.query_params.get("scope", "").split()
                if request.query_params.get("scope")
                else []
            ),
        )
        return RedirectResponse(f"/login?session={session_id}")

    async def handle_login(request: Request) -> Response:
        if request.method == "GET":
            session_id = request.query_params.get("session", "")
            return HTMLResponse(
                LOGIN_PAGE_HTML.format(session_id=session_id, error="")
            )
        form = await request.form()
        session_id = str(form.get("session", ""))
        password = str(form.get("password", ""))
        if not secrets.compare_digest(password, auth_token):
            return HTMLResponse(
                LOGIN_PAGE_HTML.format(
                    session_id=session_id,
                    error='<p class="error">Invalid password. Please try again.</p>',
                ),
                status_code=403,
            )
        result = oauth.complete_authorize(session_id)
        if not result:
            return HTMLResponse("Invalid or expired session.", status_code=400)
        code, redirect_uri, state = result
        params: Dict[str, str] = {"code": code}
        if state:
            params["state"] = state
        return RedirectResponse(
            f"{redirect_uri}?{urlencode(params)}", status_code=302
        )

    async def handle_token(request: Request) -> Response:
        form = await request.form()
        grant_type = form.get("grant_type")
        client_id = str(form.get("client_id", ""))
        if grant_type == "authorization_code":
            tokens, error = oauth.exchange_code(
                code=str(form.get("code", "")),
                client_id=client_id,
                code_verifier=str(form.get("code_verifier", "")),
                redirect_uri=str(form.get("redirect_uri", "")),
            )
        elif grant_type == "refresh_token":
            tokens, error = oauth.refresh(
                refresh_token_str=str(form.get("refresh_token", "")),
                client_id=client_id,
            )
        else:
            return JSONResponse(
                {"error": "unsupported_grant_type"}, status_code=400
            )
        if error:
            return JSONResponse({"error": error}, status_code=400)
        return JSONResponse(tokens)

    class McpEndpoint:
        """ASGI app that wraps the MCP session manager with OAuth token validation.

        Defined as a class (not a function) so that Starlette's Route treats it
        as a raw ASGI application instead of wrapping it in request_response().
        """

        async def __call__(self, scope, receive, send):
            request = Request(scope, receive, send)
            server_url = str(request.base_url).rstrip("/")
            www_auth = f'Bearer resource_metadata="{server_url}/.well-known/oauth-protected-resource"'
            auth_header = request.headers.get("authorization", "")
            if not auth_header.startswith("Bearer "):
                response = JSONResponse(
                    {"error": "Missing bearer token"},
                    status_code=401,
                    headers={"WWW-Authenticate": www_auth},
                )
                await response(scope, receive, send)
                return
            token = auth_header[len("Bearer ") :]
            if not oauth.validate_token(token):
                response = JSONResponse(
                    {"error": "Invalid or expired token"},
                    status_code=401,
                    headers={"WWW-Authenticate": www_auth},
                )
                await response(scope, receive, send)
                return
            await session_manager.handle_request(scope, receive, send)

    handle_mcp = McpEndpoint()

    async def handle_health(request: Request) -> Response:
        return JSONResponse({"status": "ok", "server": "trello-mcp"})

    @contextlib.asynccontextmanager
    async def lifespan(starlette_app: Starlette) -> AsyncIterator[None]:
        async with session_manager.run():
            yield

    return Starlette(
        routes=[
            Route(
                "/.well-known/oauth-authorization-server",
                endpoint=handle_oauth_metadata,
                methods=["GET"],
            ),
            Route(
                "/.well-known/oauth-protected-resource",
                endpoint=handle_protected_resource_metadata,
                methods=["GET"],
            ),
            Route("/register", endpoint=handle_register, methods=["GET", "POST"]),
            Route("/authorize", endpoint=handle_authorize, methods=["GET"]),
            Route("/login", endpoint=handle_login, methods=["GET", "POST"]),
            Route("/token", endpoint=handle_token, methods=["POST"]),
            Route("/health", endpoint=handle_health, methods=["GET"]),
            Route("/mcp", endpoint=handle_mcp, methods=["GET", "POST", "DELETE"]),
        ],
        lifespan=lifespan,
    )
