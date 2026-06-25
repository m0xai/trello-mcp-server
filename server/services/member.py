"""
Service for managing Trello members in MCP server.
"""

from typing import List

from server.models import TrelloMember
from server.utils.trello_api import TrelloClient


class MemberService:
    """
    Service class for managing Trello members
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_board_members(self, board_id: str) -> List[TrelloMember]:
        """Retrieves all members of a board.

        Args:
            board_id (str): The ID of the board.

        Returns:
            List[TrelloMember]: A list of member objects.
        """
        response = await self.client.GET(f"/boards/{board_id}/members")
        return [TrelloMember(**member) for member in response]

    async def add_board_member(self, board_id: str, **kwargs) -> TrelloMember:
        """Add a member to a board.

        Args:
            board_id (str): The ID of the board.
            **kwargs: Member parameters (email, type, allowBillableGuest)

        Returns:
            TrelloMember: The added member object.
        """
        response = await self.client.PUT(f"/boards/{board_id}/members", params=kwargs)
        return TrelloMember(**response)

    async def update_board_member(
        self, board_id: str, member_id: str, **kwargs
    ) -> TrelloMember:
        """Update a board member's role.

        Args:
            board_id (str): The ID of the board.
            member_id (str): The ID of the member.
            **kwargs: Update parameters (type)

        Returns:
            TrelloMember: The updated member object.
        """
        response = await self.client.PUT(
            f"/boards/{board_id}/members/{member_id}", params=kwargs
        )
        return TrelloMember(**response)

    async def remove_board_member(self, board_id: str, member_id: str) -> dict:
        """Remove a member from a board.

        Args:
            board_id (str): The ID of the board.
            member_id (str): The ID of the member to remove.

        Returns:
            dict: Response from the API.
        """
        response = await self.client.DELETE(f"/boards/{board_id}/members/{member_id}")
        return response

    async def get_workspace_members(self, workspace_id: str) -> List[TrelloMember]:
        """Retrieves all members of a workspace/organization.

        Args:
            workspace_id (str): The ID of the workspace.

        Returns:
            List[TrelloMember]: A list of member objects.
        """
        response = await self.client.GET(f"/organizations/{workspace_id}/members")
        return [TrelloMember(**member) for member in response]

    async def get_member(self, member_id: str) -> TrelloMember:
        """Retrieves a specific member by ID.

        Args:
            member_id (str): The ID of the member (or "me" for authenticated user).

        Returns:
            TrelloMember: The member object.
        """
        response = await self.client.GET(f"/members/{member_id}")
        return TrelloMember(**response)

    async def get_card_members(self, card_id: str) -> List[TrelloMember]:
        """Retrieves all members assigned to a card.

        Args:
            card_id (str): The ID of the card.

        Returns:
            List[TrelloMember]: A list of member objects.
        """
        response = await self.client.GET(f"/cards/{card_id}/members")
        return [TrelloMember(**member) for member in response]

    async def add_card_member(self, card_id: str, member_id: str) -> List[TrelloMember]:
        """Add a member to a card.

        Args:
            card_id (str): The ID of the card.
            member_id (str): The ID of the member to add.

        Returns:
            List[TrelloMember]: Updated list of card members.
        """
        response = await self.client.POST(
            f"/cards/{card_id}/idMembers", params={"value": member_id}
        )
        return [TrelloMember(**member) for member in response]

    async def remove_card_member(self, card_id: str, member_id: str) -> dict:
        """Remove a member from a card.

        Args:
            card_id (str): The ID of the card.
            member_id (str): The ID of the member to remove.

        Returns:
            dict: Response from the API.
        """
        response = await self.client.DELETE(f"/cards/{card_id}/idMembers/{member_id}")
        return response
