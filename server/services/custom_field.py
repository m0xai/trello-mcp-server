"""
Service for managing Trello custom fields.
"""

from typing import List, Dict, Any
from server.utils.trello_api import TrelloClient
from server.models.custom_field import TrelloCustomField, TrelloCustomFieldItem
from server.dtos.create_custom_field import CreateCustomFieldPayload
from server.dtos.set_custom_field_value import SetCustomFieldValuePayload


class CustomFieldService:
    """Service for custom field operations."""

    def __init__(self, client: TrelloClient):
        """
        Initialize the custom field service.

        Args:
            client: Trello API client instance
        """
        self.client = client

    def get_board_custom_fields(self, board_id: str) -> List[TrelloCustomField]:
        """
        Get all custom fields on a board.

        Args:
            board_id: The ID of the board

        Returns:
            List of TrelloCustomField objects
        """
        response = self.client.get(f"/boards/{board_id}/customFields")
        return [TrelloCustomField(**field) for field in response]

    def create_custom_field(self, payload: CreateCustomFieldPayload) -> TrelloCustomField:
        """
        Create a new custom field on a board.

        Args:
            payload: Custom field creation payload

        Returns:
            Created TrelloCustomField object
        """
        params = payload.to_api_params()
        response = self.client.post("/customFields", json=params)
        return TrelloCustomField(**response)

    def update_custom_field(
        self, 
        field_id: str, 
        name: str = None, 
        pos: str = None
    ) -> TrelloCustomField:
        """
        Update a custom field.

        Args:
            field_id: The ID of the custom field
            name: New name for the field
            pos: New position for the field

        Returns:
            Updated TrelloCustomField object
        """
        params = {}
        if name is not None:
            params["name"] = name
        if pos is not None:
            params["pos"] = pos

        response = self.client.put(f"/customFields/{field_id}", params=params)
        return TrelloCustomField(**response)

    def delete_custom_field(self, field_id: str) -> None:
        """
        Delete a custom field.

        Args:
            field_id: The ID of the custom field
        """
        self.client.delete(f"/customFields/{field_id}")

    def get_card_custom_field_items(self, card_id: str) -> List[TrelloCustomFieldItem]:
        """
        Get all custom field values on a card.

        Args:
            card_id: The ID of the card

        Returns:
            List of TrelloCustomFieldItem objects
        """
        response = self.client.get(f"/cards/{card_id}/customFieldItems")
        return [TrelloCustomFieldItem(**item) for item in response]

    def set_custom_field_value(
        self, 
        card_id: str, 
        field_id: str, 
        payload: SetCustomFieldValuePayload
    ) -> TrelloCustomFieldItem:
        """
        Set a custom field value on a card.

        Args:
            card_id: The ID of the card
            field_id: The ID of the custom field
            payload: Value payload

        Returns:
            Updated TrelloCustomFieldItem object
        """
        params = payload.to_api_params()
        response = self.client.put(
            f"/cards/{card_id}/customField/{field_id}/item",
            json=params
        )
        return TrelloCustomFieldItem(**response)

    def add_custom_field_option(
        self, 
        field_id: str, 
        text: str, 
        color: str = "none", 
        pos: str = "bottom"
    ) -> Dict[str, Any]:
        """
        Add an option to a list-type custom field.

        Args:
            field_id: The ID of the custom field
            text: The text for the option
            color: The color for the option
            pos: The position for the option

        Returns:
            Created option object
        """
        params = {
            "value": {"text": text},
            "color": color,
            "pos": pos
        }
        response = self.client.post(f"/customFields/{field_id}/options", json=params)
        return response

    def update_custom_field_option(
        self, 
        option_id: str, 
        text: str = None, 
        color: str = None, 
        pos: str = None
    ) -> Dict[str, Any]:
        """
        Update a custom field option.

        Args:
            option_id: The ID of the option
            text: New text for the option
            color: New color for the option
            pos: New position for the option

        Returns:
            Updated option object
        """
        params = {}
        if text is not None:
            params["value"] = {"text": text}
        if color is not None:
            params["color"] = color
        if pos is not None:
            params["pos"] = pos

        response = self.client.put(f"/customFieldOptions/{option_id}", params=params)
        return response

    def delete_custom_field_option(self, option_id: str) -> None:
        """
        Delete a custom field option.

        Args:
            option_id: The ID of the option
        """
        self.client.delete(f"/customFieldOptions/{option_id}")
