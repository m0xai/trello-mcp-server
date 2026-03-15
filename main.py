import argparse
import asyncio
import logging
import os

import uvicorn
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from server.tools.tools import register_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


# Initialize MCP server
mcp = FastMCP("Trello MCP Server")

# Register tools
register_tools(mcp)


def start_claude_server():
    """Start the MCP server in Claude app mode (stdio transport)"""
    try:
        # Verify environment variables
        if not os.getenv("TRELLO_API_KEY") or not os.getenv("TRELLO_TOKEN"):
            raise ValueError(
                "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment variables"
            )

        logger.info("Starting Trello MCP Server in Claude app mode...")
        mcp.run()
        logger.info("Trello MCP Server started successfully")
    except Exception as e:
        logger.error(f"Error starting Claude server: {str(e)}")
        raise


def start_sse_server():
    """Start the MCP server in SSE mode using uvicorn"""
    from starlette.applications import Starlette
    from starlette.routing import Mount

    try:
        # Verify environment variables
        if not os.getenv("TRELLO_API_KEY") or not os.getenv("TRELLO_TOKEN"):
            raise ValueError(
                "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment variables"
            )

        host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_SERVER_PORT", "8000"))

        # Create Starlette app with MCP server mounted
        app = Starlette(
            routes=[
                Mount("/", app=mcp.sse_app()),
            ]
        )

        logger.info(
            f"Starting Trello MCP Server in SSE mode on http://{host}:{port}..."
        )
        uvicorn.run(app, host=host, port=port)
    except Exception as e:
        logger.error(f"Error starting SSE server: {str(e)}")
        raise


def start_http_server(host: str, port: int):
    """Start the MCP server in SSE mode with OAuth 2.0 authentication."""
    from server.oauth import create_http_app

    try:
        # Verify environment variables
        if not os.getenv("TRELLO_API_KEY") or not os.getenv("TRELLO_TOKEN"):
            raise ValueError(
                "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment variables"
            )

        auth_token = os.getenv("MCP_AUTH_TOKEN")
        if not auth_token:
            raise ValueError(
                "MCP_AUTH_TOKEN environment variable is required for HTTP transport"
            )

        http_app = create_http_app(mcp._mcp_server, auth_token)

        logger.info(
            f"Starting Trello MCP Server in HTTP mode on http://{host}:{port}..."
        )
        uvicorn.run(
            http_app,
            host=host,
            port=port,
            proxy_headers=True,
            forwarded_allow_ips="*",
        )
    except Exception as e:
        logger.error(f"Error starting HTTP server: {str(e)}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trello MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "http"],
        default="stdio",
        help="Transport mode: stdio (local), sse (legacy HTTP), or http (Streamable HTTP with OAuth)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (sse/http mode, default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", os.getenv("MCP_SERVER_PORT", "8000"))),
        help="Port to listen on (sse/http mode, default: PORT env or 8000)",
    )
    args = parser.parse_args()

    try:
        if args.transport == "http":
            start_http_server(args.host, args.port)
        elif args.transport == "sse":
            start_sse_server()
        else:
            start_claude_server()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise
