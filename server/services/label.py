"""
Service for managing Trello labels in MCP server.
"""

from typing import List

from server.models import TrelloLabel
from server.utils.trello_api import TrelloClient


class LabelService:
    """
    Service class for managing Trello labels
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def update_label(self, label_id: str, **kwargs) -> TrelloLabel:
        """Update a label.

        Args:
            label_id (str): The ID of the label.
            **kwargs: Update parameters (name, color)

        Returns:
            TrelloLabel: The updated label object.
        """
        response = await self.client.PUT(f"/labels/{label_id}", params=kwargs)
        return TrelloLabel(**response)

    async def delete_label(self, label_id: str) -> dict:
        """Delete a label.

        Args:
            label_id (str): The ID of the label to delete.

        Returns:
            dict: Response from the API.
        """
        response = await self.client.DELETE(f"/labels/{label_id}")
        return response

    async def get_card_labels(self, card_id: str) -> List[TrelloLabel]:
        """Retrieves all labels on a card.

        Args:
            card_id (str): The ID of the card.

        Returns:
            List[TrelloLabel]: A list of label objects.
        """
        # Get card details which include labels
        response = await self.client.GET(f"/cards/{card_id}", params={"fields": "labels"})
        labels_data = response.get("labels", [])
        return [TrelloLabel(**label) for label in labels_data]

    async def add_label_to_card(self, card_id: str, label_id: str) -> List[TrelloLabel]:
        """Add a label to a card.

        Args:
            card_id (str): The ID of the card.
            label_id (str): The ID of the label to add.

        Returns:
            List[TrelloLabel]: Updated list of labels on the card.
        """
        response = await self.client.POST(
            f"/cards/{card_id}/idLabels", params={"value": label_id}
        )
        return [TrelloLabel(**label) for label in response]

    async def remove_label_from_card(self, card_id: str, label_id: str) -> dict:
        """Remove a label from a card.

        Args:
            card_id (str): The ID of the card.
            label_id (str): The ID of the label to remove.

        Returns:
            dict: Response from the API.
        """
        response = await self.client.DELETE(f"/cards/{card_id}/idLabels/{label_id}")
        return response
