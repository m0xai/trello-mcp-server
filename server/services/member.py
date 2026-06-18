"""
Service for managing Trello members in MCP server.
"""

from server.models import TrelloMember
from server.utils.trello_api import TrelloClient


class MemberService:
    """
    Service class for managing Trello members.
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_member(self, member_id: str) -> TrelloMember:
        """Retrieves a member by their ID or username.

        Args:
            member_id (str): The ID or username of the member to retrieve.

        Returns:
            TrelloMember: The member object containing member details.
        """
        response = await self.client.GET(f"/members/{member_id}")
        return TrelloMember(**response)
