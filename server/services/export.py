"""
Service for Trello export and import operations.
"""

from typing import Dict, Any, List
from server.utils.trello_api import TrelloClient


class ExportService:
    """Service for export and import operations."""

    def __init__(self, client: TrelloClient):
        """
        Initialize the export service.

        Args:
            client: Trello API client instance
        """
        self.client = client

    def export_board(self, board_id: str) -> Dict[str, Any]:
        """
        Export a complete board with all data.

        Args:
            board_id: The ID of the board to export

        Returns:
            Complete board data including cards, lists, members, labels, checklists
        """
        params = {
            "fields": "all",
            "actions": "all",
            "action_fields": "all",
            "actions_limit": "1000",
            "cards": "all",
            "card_fields": "all",
            "card_attachments": "true",
            "labels": "all",
            "lists": "all",
            "list_fields": "all",
            "members": "all",
            "member_fields": "all",
            "checklists": "all",
            "checklist_fields": "all",
            "customFields": "true"
        }
        
        response = self.client.get(f"/boards/{board_id}", params=params)
        return response

    def list_organization_exports(self, org_id: str) -> List[Dict[str, Any]]:
        """
        List all exports for an organization.

        Args:
            org_id: The ID of the organization

        Returns:
            List of export objects
        """
        response = self.client.get(f"/organizations/{org_id}/exports")
        return response

    def create_organization_export(self, org_id: str, attachments: bool = True) -> Dict[str, Any]:
        """
        Create a new export for an organization.

        Args:
            org_id: The ID of the organization
            attachments: Whether to include attachments (default True)

        Returns:
            Export object with status and download URL
        """
        params = {"attachments": str(attachments).lower()}
        response = self.client.post(f"/organizations/{org_id}/exports", params=params)
        return response
