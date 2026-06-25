"""
Service for managing Trello workspaces/organizations in MCP server.
"""

from typing import List

from server.models import TrelloBoard, TrelloOrganization
from server.utils.trello_api import TrelloClient


class WorkspaceService:
    """
    Service class for managing Trello workspaces/organizations
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_workspaces(self, member_id: str = "me") -> List[TrelloOrganization]:
        """Retrieves all workspaces for a given member.

        Args:
            member_id (str): The ID of the member whose workspaces to retrieve.
                           Defaults to "me" for the authenticated user.

        Returns:
            List[TrelloOrganization]: A list of workspace/organization objects.
        """
        response = await self.client.GET(f"/members/{member_id}/organizations")
        return [TrelloOrganization(**org) for org in response]

    async def get_workspace(self, workspace_id: str) -> TrelloOrganization:
        """Retrieves a specific workspace by its ID.

        Args:
            workspace_id (str): The ID of the workspace to retrieve.

        Returns:
            TrelloOrganization: The workspace object containing workspace details.
        """
        response = await self.client.GET(f"/organizations/{workspace_id}")
        return TrelloOrganization(**response)

    async def get_workspace_boards(
        self, workspace_id: str, filter_value: str = "all"
    ) -> List[TrelloBoard]:
        """Retrieves all boards in a workspace.

        Args:
            workspace_id (str): The ID of the workspace whose boards to retrieve.
            filter_value (str): Filter for boards. Options: all, open, closed, members,
                              organization, public. Defaults to "all".

        Returns:
            List[TrelloBoard]: A list of board objects in the workspace.
        """
        params = {"filter": filter_value}
        response = await self.client.GET(
            f"/organizations/{workspace_id}/boards", params=params
        )
        return [TrelloBoard(**board) for board in response]

    async def create_workspace(self, **kwargs) -> TrelloOrganization:
        """Create a new workspace/organization.

        Args:
            **kwargs: Workspace creation parameters (displayName, desc, name, website)

        Returns:
            TrelloOrganization: The newly created workspace object.
        """
        response = await self.client.POST("/organizations", params=kwargs)
        return TrelloOrganization(**response)

    async def update_workspace(
        self, workspace_id: str, **kwargs
    ) -> TrelloOrganization:
        """Update an existing workspace.

        Args:
            workspace_id (str): The ID of the workspace to update.
            **kwargs: Workspace update parameters

        Returns:
            TrelloOrganization: The updated workspace object.
        """
        response = await self.client.PUT(f"/organizations/{workspace_id}", params=kwargs)
        return TrelloOrganization(**response)

    async def delete_workspace(self, workspace_id: str) -> dict:
        """Delete (permanently remove) a workspace/organization.

        Args:
            workspace_id (str): The ID of the workspace to delete.

        Returns:
            dict: Response from the API.
        """
        response = await self.client.DELETE(f"/organizations/{workspace_id}")
        return response
