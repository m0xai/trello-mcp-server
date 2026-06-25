"""
Service for Trello batch operations.
"""

from typing import List, Dict, Any
from server.utils.trello_api import TrelloClient


class BatchService:
    """Service for batch operations."""

    def __init__(self, client: TrelloClient):
        """
        Initialize the batch service.

        Args:
            client: Trello API client instance
        """
        self.client = client

    def batch_get(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Execute multiple GET requests in a single batch.

        Args:
            urls: List of relative URLs to fetch (max 10)

        Returns:
            List of response objects
        """
        if len(urls) > 10:
            raise ValueError("Maximum 10 URLs allowed per batch request")

        # Join URLs with comma
        urls_param = ",".join(urls)
        
        response = self.client.get("/batch", params={"urls": urls_param})
        return response
