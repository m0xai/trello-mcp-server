# trello_api.py
import logging

import httpx

# Configure logging
logger = logging.getLogger(__name__)

TRELLO_API_BASE = "https://api.trello.com/1"


class TrelloClient:
    """
    Client class for interacting with the Trello API over REST.
    """

    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token
        self.base_url = TRELLO_API_BASE
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def close(self):
        await self.client.aclose()

    async def GET(self, endpoint: str, params: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        if params:
            all_params.update(params)
        try:
            response = await self.client.get(endpoint, params=all_params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise httpx.HTTPStatusError(
                f"Failed to get {endpoint}: {str(e)}",
                request=e.request,
                response=e.response,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise httpx.RequestError(f"Failed to get {endpoint}: {str(e)}")

    async def POST(self, endpoint: str, data: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        try:
            response = await self.client.post(endpoint, params=all_params, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise httpx.HTTPStatusError(
                f"Failed to post to {endpoint}: {str(e)}",
                request=e.request,
                response=e.response,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise httpx.RequestError(f"Failed to post to {endpoint}: {str(e)}")

    async def PUT(self, endpoint: str, data: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        try:
            response = await self.client.put(endpoint, params=all_params, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise httpx.HTTPStatusError(
                f"Failed to put to {endpoint}: {str(e)}",
                request=e.request,
                response=e.response,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise httpx.RequestError(f"Failed to put to {endpoint}: {str(e)}")

    async def POST_FORM(self, endpoint: str, data: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        try:
            response = await self.client.post(endpoint, params=all_params, data=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise httpx.HTTPStatusError(
                f"Failed to post form to {endpoint}: {str(e)}",
                request=e.request,
                response=e.response,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise httpx.RequestError(f"Failed to post form to {endpoint}: {str(e)}")

    async def DELETE(self, endpoint: str, params: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        if params:
            all_params.update(params)
        try:
            response = await self.client.delete(endpoint, params=all_params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise httpx.HTTPStatusError(
                f"Failed to delete {endpoint}: {str(e)}",
                request=e.request,
                response=e.response,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise httpx.RequestError(f"Failed to delete {endpoint}: {str(e)}")
