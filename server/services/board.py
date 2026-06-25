"""
Service for managing Trello boards in MCP server.
"""

from typing import List

from server.models import TrelloBoard, TrelloLabel
from server.utils.trello_api import TrelloClient


class BoardService:
    """
    Service class for managing Trello boards
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_board(self, board_id: str) -> TrelloBoard:
        """Retrieves a specific board by its ID.

        Args:
            board_id (str): The ID of the board to retrieve.

        Returns:
            TrelloBoard: The board object containing board details.
        """
        response = await self.client.GET(f"/boards/{board_id}")
        return TrelloBoard(**response)

    async def get_boards(self, member_id: str = "me") -> List[TrelloBoard]:
        """Retrieves all boards for a given member.

        Args:
            member_id (str): The ID of the member whose boards to retrieve. Defaults to "me" for the authenticated user.

        Returns:
            List[TrelloBoard]: A list of board objects.
        """
        response = await self.client.GET(f"/members/{member_id}/boards")
        return [TrelloBoard(**board) for board in response]

    async def get_board_labels(self, board_id: str) -> List[TrelloLabel]:
        """Retrieves all labels for a specific board.

        Args:
            board_id (str): The ID of the board whose labels to retrieve.

        Returns:
            List[TrelloLabel]: A list of label objects for the board.
        """
        response = await self.client.GET(f"/boards/{board_id}/labels")
        return [TrelloLabel(**label) for label in response]

    async def create_board_label(self, board_id: str, **kwargs) -> TrelloLabel:
        """Create label for a specific board.

        Args:
            board_id (str): The ID of the board whose to add label.

        Returns:
            TrelloLabel: A label object for the board.
        """
        response = await self.client.POST(f"/boards/{board_id}/labels", data=kwargs)
        return TrelloLabel(**response)

    async def create_board(self, **kwargs) -> TrelloBoard:
        """Create a new board.

        Args:
            **kwargs: Board creation parameters (name, desc, idOrganization, etc.)

        Returns:
            TrelloBoard: The newly created board object.
        """
        # Convert Python naming to Trello API naming
        params = {}
        if "name" in kwargs:
            params["name"] = kwargs["name"]
        if "desc" in kwargs:
            params["desc"] = kwargs["desc"]
        if "id_organization" in kwargs and kwargs["id_organization"]:
            params["idOrganization"] = kwargs["id_organization"]
        if "default_lists" in kwargs:
            params["defaultLists"] = kwargs["default_lists"]
        if "default_labels" in kwargs:
            params["defaultLabels"] = kwargs["default_labels"]
        if "prefs_permission_level" in kwargs:
            params["prefs_permissionLevel"] = kwargs["prefs_permission_level"]
        if "prefs_voting" in kwargs and kwargs["prefs_voting"]:
            params["prefs_voting"] = kwargs["prefs_voting"]
        if "prefs_comments" in kwargs and kwargs["prefs_comments"]:
            params["prefs_comments"] = kwargs["prefs_comments"]

        response = await self.client.POST("/boards", params=params)
        return TrelloBoard(**response)

    async def update_board(self, board_id: str, **kwargs) -> TrelloBoard:
        """Update an existing board.

        Args:
            board_id (str): The ID of the board to update.
            **kwargs: Board update parameters

        Returns:
            TrelloBoard: The updated board object.
        """
        response = await self.client.PUT(f"/boards/{board_id}", params=kwargs)
        return TrelloBoard(**response)

    async def delete_board(self, board_id: str) -> dict:
        """Delete (permanently remove) a board.

        Args:
            board_id (str): The ID of the board to delete.

        Returns:
            dict: Response from the API.
        """
        response = await self.client.DELETE(f"/boards/{board_id}")
        return response
