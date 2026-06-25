# trello_api.py
import asyncio
import logging
from typing import Optional

import httpx

from server.exceptions import (
    BadRequestError,
    ForbiddenError,
    RateLimitError,
    ResourceNotFoundError,
    TrelloMCPError,
    UnauthorizedError,
)

# Configure logging
logger = logging.getLogger(__name__)

TRELLO_API_BASE = "https://api.trello.com/1"


class TrelloClient:
    """
    Client class for interacting with the Trello API over REST.
    Includes enhanced error handling, retry logic, and rate limit management.
    """

    def __init__(self, api_key: str, token: str, max_retries: int = 3):
        self.api_key = api_key
        self.token = token
        self.base_url = TRELLO_API_BASE
        self.max_retries = max_retries
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    async def close(self):
        await self.client.aclose()

    def _handle_http_error(
        self, error: httpx.HTTPStatusError, endpoint: str, method: str
    ):
        """
        Handle HTTP errors with specific exception types based on status code.

        Args:
            error: The HTTP status error
            endpoint: The API endpoint that was called
            method: The HTTP method used

        Raises:
            Specific TrelloMCPError subclass based on status code
        """
        status_code = error.response.status_code
        response_text = error.response.text

        logger.error(
            f"HTTP {status_code} error for {method} {endpoint}: {response_text}"
        )

        if status_code == 400:
            raise BadRequestError(
                f"Invalid request to {endpoint}. {response_text or 'Please check your parameters.'}"
            )
        elif status_code == 401:
            raise UnauthorizedError()
        elif status_code == 403:
            raise ForbiddenError("Resource", endpoint, "access")
        elif status_code == 404:
            # Extract resource type from endpoint
            resource_type = endpoint.split("/")[1].rstrip("s").capitalize()
            resource_id = endpoint.split("/")[2] if len(endpoint.split("/")) > 2 else "unknown"
            raise ResourceNotFoundError(resource_type, resource_id)
        elif status_code == 429:
            retry_after = error.response.headers.get("Retry-After")
            raise RateLimitError(
                retry_after=int(retry_after) if retry_after else None
            )
        else:
            raise TrelloMCPError(
                f"HTTP {status_code} error for {method} {endpoint}: {response_text}",
                status_code=status_code,
            )

    async def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ):
        """
        Execute a request with exponential backoff retry for rate limits.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response JSON

        Raises:
            TrelloMCPError or subclass on failure
        """
        base_delay = 1

        for attempt in range(self.max_retries):
            try:
                if method == "GET":
                    return await self._get(endpoint, params)
                elif method == "POST":
                    return await self._post(endpoint, params, data)
                elif method == "PUT":
                    return await self._put(endpoint, params, data)
                elif method == "DELETE":
                    return await self._delete(endpoint, params)
            except RateLimitError as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Max retries exceeded for {method} {endpoint}")
                    raise

                delay = e.retry_after or (base_delay * (2**attempt))
                logger.warning(
                    f"Rate limit hit on attempt {attempt + 1}/{self.max_retries}. "
                    f"Retrying in {delay} seconds..."
                )
                await asyncio.sleep(delay)
            except (httpx.RequestError, httpx.TimeoutException) as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Max retries exceeded for {method} {endpoint}")
                    raise TrelloMCPError(
                        f"Network error after {self.max_retries} attempts: {str(e)}"
                    )

                delay = base_delay * (2**attempt)
                logger.warning(
                    f"Network error on attempt {attempt + 1}/{self.max_retries}. "
                    f"Retrying in {delay} seconds... Error: {str(e)}"
                )
                await asyncio.sleep(delay)

        raise TrelloMCPError(f"Max retries exceeded for {method} {endpoint}")

    async def _get(self, endpoint: str, params: Optional[dict] = None):
        """Internal GET method without retry logic."""
        all_params = {"key": self.api_key, "token": self.token}
        if params:
            all_params.update(params)

        try:
            response = await self.client.get(endpoint, params=all_params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e, endpoint, "GET")
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise

    async def _post(
        self, endpoint: str, params: Optional[dict] = None, data: Optional[dict] = None
    ):
        """Internal POST method without retry logic."""
        all_params = {"key": self.api_key, "token": self.token}
        if params:
            all_params.update(params)

        try:
            response = await self.client.post(endpoint, params=all_params, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e, endpoint, "POST")
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise

    async def _put(
        self, endpoint: str, params: Optional[dict] = None, data: Optional[dict] = None
    ):
        """Internal PUT method without retry logic."""
        all_params = {"key": self.api_key, "token": self.token}
        if params:
            all_params.update(params)

        try:
            response = await self.client.put(endpoint, params=all_params, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e, endpoint, "PUT")
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise

    async def _delete(self, endpoint: str, params: Optional[dict] = None):
        """Internal DELETE method without retry logic."""
        all_params = {"key": self.api_key, "token": self.token}
        if params:
            all_params.update(params)

        try:
            response = await self.client.delete(endpoint, params=all_params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e, endpoint, "DELETE")
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise

    # Public methods with retry logic
    async def GET(self, endpoint: str, params: Optional[dict] = None):
        """
        Execute a GET request with retry logic.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response JSON
        """
        return await self._request_with_retry("GET", endpoint, params=params)

    async def POST(
        self, endpoint: str, data: Optional[dict] = None, params: Optional[dict] = None
    ):
        """
        Execute a POST request with retry logic.

        Args:
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response JSON
        """
        return await self._request_with_retry("POST", endpoint, params=params, data=data)

    async def PUT(
        self, endpoint: str, data: Optional[dict] = None, params: Optional[dict] = None
    ):
        """
        Execute a PUT request with retry logic.

        Args:
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response JSON
        """
        return await self._request_with_retry("PUT", endpoint, params=params, data=data)

    async def DELETE(self, endpoint: str, params: Optional[dict] = None):
        """
        Execute a DELETE request with retry logic.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response JSON
        """
        return await self._request_with_retry("DELETE", endpoint, params=params)
