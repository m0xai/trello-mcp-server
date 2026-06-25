"""
Service for managing Trello comments and actions in MCP server.
"""

from typing import List

from server.models import TrelloAction
from server.utils.trello_api import TrelloClient


class CommentService:
    """
    Service class for managing Trello comments and actions
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_card_comments(self, card_id: str) -> List[TrelloAction]:
        """Retrieves all comments on a card.

        Args:
            card_id (str): The ID of the card.

        Returns:
            List[TrelloAction]: A list of comment actions.
        """
        response = await self.client.GET(
            f"/cards/{card_id}/actions", params={"filter": "commentCard"}
        )
        return [TrelloAction(**action) for action in response]

    async def get_card_actions(
        self, card_id: str, filter: str = "all", limit: int = 50
    ) -> List[TrelloAction]:
        """Retrieves actions/activity on a card.

        Args:
            card_id (str): The ID of the card.
            filter (str): Filter for action types (default: "all").
            limit (int): Maximum number of actions to return (default: 50).

        Returns:
            List[TrelloAction]: A list of action objects.
        """
        response = await self.client.GET(
            f"/cards/{card_id}/actions", params={"filter": filter, "limit": limit}
        )
        return [TrelloAction(**action) for action in response]

    async def add_comment(self, card_id: str, **kwargs) -> TrelloAction:
        """Add a comment to a card.

        Args:
            card_id (str): The ID of the card.
            **kwargs: Comment parameters (text)

        Returns:
            TrelloAction: The created comment action.
        """
        response = await self.client.POST(
            f"/cards/{card_id}/actions/comments", params=kwargs
        )
        return TrelloAction(**response)

    async def update_comment(self, action_id: str, **kwargs) -> TrelloAction:
        """Update a comment.

        Args:
            action_id (str): The ID of the comment action.
            **kwargs: Update parameters (text)

        Returns:
            TrelloAction: The updated comment action.
        """
        response = await self.client.PUT(f"/actions/{action_id}", params=kwargs)
        return TrelloAction(**response)

    async def delete_comment(self, action_id: str) -> dict:
        """Delete a comment.

        Args:
            action_id (str): The ID of the comment action to delete.

        Returns:
            dict: Response from the API.
        """
        response = await self.client.DELETE(f"/actions/{action_id}")
        return response

    async def get_board_actions(
        self, board_id: str, filter: str = "all", limit: int = 50
    ) -> List[TrelloAction]:
        """Retrieves actions/activity on a board.

        Args:
            board_id (str): The ID of the board.
            filter (str): Filter for action types (default: "all").
            limit (int): Maximum number of actions to return (default: 50).

        Returns:
            List[TrelloAction]: A list of action objects.
        """
        response = await self.client.GET(
            f"/boards/{board_id}/actions", params={"filter": filter, "limit": limit}
        )
        return [TrelloAction(**action) for action in response]
