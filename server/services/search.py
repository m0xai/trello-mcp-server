"""
Service for Trello search operations.
"""

from typing import List, Optional, Dict, Any
from server.utils.trello_api import TrelloClient


class SearchService:
    """Service for search and filtering operations."""

    def __init__(self, client: TrelloClient):
        """
        Initialize the search service.

        Args:
            client: Trello API client instance
        """
        self.client = client

    def search(
        self,
        query: str,
        id_boards: Optional[str] = None,
        id_organizations: Optional[str] = None,
        model_types: Optional[str] = None,
        partial: bool = False
    ) -> Dict[str, Any]:
        """
        Search across Trello resources.

        Args:
            query: Search query string
            id_boards: Comma-separated list of board IDs to search
            id_organizations: Comma-separated list of organization IDs to search
            model_types: Comma-separated list of model types (cards, boards, members, organizations)
            partial: Enable partial matching

        Returns:
            Dictionary containing search results by type
        """
        params = {"query": query}
        
        if id_boards:
            params["idBoards"] = id_boards
        if id_organizations:
            params["idOrganizations"] = id_organizations
        if model_types:
            params["modelTypes"] = model_types
        if partial:
            params["partial"] = "true"

        response = self.client.get("/search", params=params)
        return response

    def search_members(self, query: str, limit: int = 8) -> List[Dict[str, Any]]:
        """
        Search for members.

        Args:
            query: Search query string
            limit: Maximum number of results (default 8, max 20)

        Returns:
            List of member objects
        """
        params = {
            "query": query,
            "limit": min(limit, 20)
        }

        response = self.client.get("/search/members", params=params)
        return response
