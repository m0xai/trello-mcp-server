"""
Service for managing Trello attachments in MCP server.
"""

from typing import List

from server.models import TrelloAttachment
from server.utils.trello_api import TrelloClient


class AttachmentService:
    """
    Service class for managing Trello attachments
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_card_attachments(self, card_id: str) -> List[TrelloAttachment]:
        """Retrieves all attachments on a card.

        Args:
            card_id (str): The ID of the card.

        Returns:
            List[TrelloAttachment]: A list of attachment objects.
        """
        response = await self.client.GET(f"/cards/{card_id}/attachments")
        return [TrelloAttachment(**attachment) for attachment in response]

    async def attach_url(self, card_id: str, **kwargs) -> TrelloAttachment:
        """Attach a URL to a card.

        Args:
            card_id (str): The ID of the card.
            **kwargs: Attachment parameters (url, name)

        Returns:
            TrelloAttachment: The created attachment object.
        """
        response = await self.client.POST(
            f"/cards/{card_id}/attachments", params=kwargs
        )
        return TrelloAttachment(**response)

    async def upload_attachment(
        self, card_id: str, file_path: str, name: str = None
    ) -> TrelloAttachment:
        """Upload a file attachment to a card.

        Args:
            card_id (str): The ID of the card.
            file_path (str): Path to the file to upload.
            name (str): Optional display name for the attachment.

        Returns:
            TrelloAttachment: The created attachment object.
        """
        # Note: This requires multipart/form-data support in TrelloClient
        # For now, we'll use the file parameter approach
        params = {}
        if name:
            params["name"] = name
        
        # The actual file upload would need special handling
        # This is a placeholder for the implementation
        response = await self.client.POST(
            f"/cards/{card_id}/attachments",
            params=params,
            files={"file": file_path}
        )
        return TrelloAttachment(**response)

    async def get_attachment(self, card_id: str, attachment_id: str) -> TrelloAttachment:
        """Retrieves a specific attachment.

        Args:
            card_id (str): The ID of the card.
            attachment_id (str): The ID of the attachment.

        Returns:
            TrelloAttachment: The attachment object.
        """
        response = await self.client.GET(
            f"/cards/{card_id}/attachments/{attachment_id}"
        )
        return TrelloAttachment(**response)

    async def delete_attachment(self, card_id: str, attachment_id: str) -> dict:
        """Delete an attachment from a card.

        Args:
            card_id (str): The ID of the card.
            attachment_id (str): The ID of the attachment to delete.

        Returns:
            dict: Response from the API.
        """
        response = await self.client.DELETE(
            f"/cards/{card_id}/attachments/{attachment_id}"
        )
        return response

    async def set_attachment_as_cover(
        self, card_id: str, attachment_id: str
    ) -> dict:
        """Set an attachment as the card cover.

        Args:
            card_id (str): The ID of the card.
            attachment_id (str): The ID of the attachment.

        Returns:
            dict: Response from the API.
        """
        response = await self.client.PUT(
            f"/cards/{card_id}",
            params={"idAttachmentCover": attachment_id}
        )
        return response
