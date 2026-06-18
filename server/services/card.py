"""
Service for managing Trello cards in MCP server.
"""

from typing import Any, Dict, List

from server.models import TrelloCard
from server.utils.trello_api import TrelloClient


class CardService:
    """
    Service class for managing Trello cards.
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_card(self, card_id: str) -> TrelloCard:
        """Retrieves a specific card by its ID.

        Args:
            card_id (str): The ID of the card to retrieve.

        Returns:
            TrelloCard: The card object containing card details.
        """
        response = await self.client.GET(f"/cards/{card_id}", params={"attachments": "true"})
        return TrelloCard(**response)

    async def get_cards(
        self,
        list_id: str,
        member_id: str | None = None,
        label_id: str | None = None,
    ) -> List[TrelloCard]:
        """Retrieves all cards in a given list with optional client-side filtering.

        Args:
            list_id (str): The ID of the list whose cards to retrieve.
            member_id (str, optional): Filter cards assigned to this member ID.
            label_id (str, optional): Filter cards that have this label ID.

        Returns:
            List[TrelloCard]: A list of card objects.
        """
        response = await self.client.GET(f"/lists/{list_id}/cards")
        cards = [TrelloCard(**card) for card in response]
        if member_id:
            cards = [c for c in cards if member_id in c.idMembers]
        if label_id:
            cards = [c for c in cards if any(label.id == label_id for label in c.labels)]
        return cards

    async def create_card(self, **kwargs) -> TrelloCard:
        """Creates a new card in a given list.

        Args
            list_id (str): The ID of the list to create the card in.
            name (str): The name of the new card.
            desc (str, optional): The description of the new card. Defaults to None.

        Returns:
            TrelloCard: The newly created card object.
        """
        response = await self.client.POST("/cards", data=kwargs)
        return TrelloCard(**response)

    async def update_card(self, card_id: str, **kwargs) -> TrelloCard:
        """Updates a card's attributes.

        Args:
            card_id (str): The ID of the card to update.
            **kwargs: Keyword arguments representing the attributes to update on the card.

        Returns:
            TrelloCard: The updated card object.
        """
        response = await self.client.PUT(f"/cards/{card_id}", data=kwargs)
        return TrelloCard(**response)

    async def delete_card(self, card_id: str) -> Dict[str, Any]:
        """Deletes a card.

        Args:
            card_id (str): The ID of the card to delete.

        Returns:
            Dict[str, Any]: The response from the delete operation.
        """
        return await self.client.DELETE(f"/cards/{card_id}")

    async def archive_card(self, card_id: str) -> TrelloCard:
        """Archives a card (sets closed=True). Different from delete — card is preserved.

        Args:
            card_id (str): The ID of the card to archive.

        Returns:
            TrelloCard: The archived card object.
        """
        response = await self.client.PUT(f"/cards/{card_id}", data={"closed": True})
        return TrelloCard(**response)

    async def get_card_comments(self, card_id: str) -> List[Dict[str, Any]]:
        """Retrieves all comments on a card.

        Args:
            card_id (str): The ID of the card.

        Returns:
            List[Dict[str, Any]]: A list of comment action objects.
        """
        return await self.client.GET(f"/cards/{card_id}/actions", params={"filter": "commentCard"})

    async def add_comment_to_card(self, card_id: str, text: str) -> Dict[str, Any]:
        """Adds a comment to a card.

        Args:
            card_id (str): The ID of the card.
            text (str): The comment text.

        Returns:
            Dict[str, Any]: The created comment action object.
        """
        return await self.client.POST(f"/cards/{card_id}/actions/comments", data={"text": text})

    async def add_member_to_card(self, card_id: str, member_id: str) -> List[str]:
        """Adds a member to a card.

        Args:
            card_id (str): The ID of the card.
            member_id (str): The ID of the member to add.

        Returns:
            List[str]: The updated list of member IDs on the card.
        """
        response = await self.client.POST(f"/cards/{card_id}/idMembers", data={"value": member_id})
        return response

    async def remove_member_from_card(self, card_id: str, member_id: str) -> Dict[str, Any]:
        """Removes a member from a card.

        Args:
            card_id (str): The ID of the card.
            member_id (str): The ID of the member to remove.

        Returns:
            Dict[str, Any]: The response from the remove operation.
        """
        return await self.client.DELETE(f"/cards/{card_id}/idMembers/{member_id}")

    async def search_cards(self, query: str, board_id: str | None = None) -> List[TrelloCard]:
        """Searches for cards matching a query, optionally scoped to a board.

        Args:
            query (str): The search query string.
            board_id (str, optional): Limit results to this board ID.

        Returns:
            List[TrelloCard]: A list of matching card objects.
        """
        params: Dict[str, Any] = {"query": query, "modelTypes": "cards"}
        if board_id:
            params["idBoards"] = board_id
        response = await self.client.GET("/search", params=params)
        return [TrelloCard(**card) for card in response.get("cards", [])]
