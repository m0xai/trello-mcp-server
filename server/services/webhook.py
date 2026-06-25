"""
Service for managing Trello webhooks in MCP server.
"""

from typing import List

from server.models import TrelloWebhook
from server.utils.trello_api import TrelloClient


class WebhookService:
    """
    Service class for managing Trello webhooks
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def create_webhook(self, **kwargs) -> TrelloWebhook:
        """Create a new webhook.

        Args:
            **kwargs: Webhook parameters (callbackURL, idModel, description, active)

        Returns:
            TrelloWebhook: The created webhook object.
        """
        response = await self.client.POST("/webhooks/", params=kwargs)
        return TrelloWebhook(**response)

    async def get_webhook(self, webhook_id: str) -> TrelloWebhook:
        """Retrieves a specific webhook by ID.

        Args:
            webhook_id (str): The ID of the webhook.

        Returns:
            TrelloWebhook: The webhook object.
        """
        response = await self.client.GET(f"/webhooks/{webhook_id}")
        return TrelloWebhook(**response)

    async def list_webhooks(self, token: str) -> List[TrelloWebhook]:
        """Retrieves all webhooks for a token.

        Args:
            token (str): The API token.

        Returns:
            List[TrelloWebhook]: A list of webhook objects.
        """
        response = await self.client.GET(f"/tokens/{token}/webhooks")
        return [TrelloWebhook(**webhook) for webhook in response]

    async def update_webhook(self, webhook_id: str, **kwargs) -> TrelloWebhook:
        """Update a webhook.

        Args:
            webhook_id (str): The ID of the webhook.
            **kwargs: Update parameters (callbackURL, description, active)

        Returns:
            TrelloWebhook: The updated webhook object.
        """
        response = await self.client.PUT(f"/webhooks/{webhook_id}", params=kwargs)
        return TrelloWebhook(**response)

    async def delete_webhook(self, webhook_id: str) -> dict:
        """Delete a webhook.

        Args:
            webhook_id (str): The ID of the webhook to delete.

        Returns:
            dict: Response from the API.
        """
        response = await self.client.DELETE(f"/webhooks/{webhook_id}")
        return response
