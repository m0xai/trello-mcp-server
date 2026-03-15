"""
Service for managing Trello card comments and attachments.
"""

from typing import Any, Dict, List

from server.models import TrelloAttachment, TrelloComment
from server.utils.trello_api import TrelloClient


class CommentService:
    """
    Service class for managing Trello card comments and attachments.
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_comments(self, card_id: str) -> List[TrelloComment]:
        """Retrieves all comments on a card.

        Args:
            card_id: The ID of the card.

        Returns:
            List of comment action objects.
        """
        response = await self.client.GET(
            f"/cards/{card_id}/actions",
            params={"filter": "commentCard"},
        )
        return [TrelloComment(**action) for action in response]

    async def add_comment(self, card_id: str, text: str) -> TrelloComment:
        """Adds a comment to a card.

        Args:
            card_id: The ID of the card.
            text: The comment text. Supports Trello markdown and @mentions.

        Returns:
            The created comment action object.
        """
        response = await self.client.POST(
            f"/cards/{card_id}/actions/comments",
            data={"text": text},
        )
        return TrelloComment(**response)

    async def update_comment(self, card_id: str, action_id: str, text: str) -> TrelloComment:
        """Updates an existing comment on a card.

        Args:
            card_id: The ID of the card the comment belongs to.
            action_id: The ID of the comment action to update.
            text: The new comment text.

        Returns:
            The updated comment action object.
        """
        response = await self.client.PUT(
            f"/cards/{card_id}/actions/{action_id}/comments",
            data={"text": text},
        )
        return TrelloComment(**response)

    async def delete_comment(self, card_id: str, action_id: str) -> Dict[str, Any]:
        """Deletes a comment from a card.

        Args:
            card_id: The ID of the card the comment belongs to.
            action_id: The ID of the comment action to delete.

        Returns:
            The response from the delete operation.
        """
        return await self.client.DELETE(
            f"/cards/{card_id}/actions/{action_id}/comments"
        )

    async def get_attachments(self, card_id: str) -> List[TrelloAttachment]:
        """Retrieves all attachments on a card.

        Args:
            card_id: The ID of the card.

        Returns:
            List of attachment objects.
        """
        response = await self.client.GET(f"/cards/{card_id}/attachments")
        return [TrelloAttachment(**att) for att in response]

    async def add_attachment(
        self,
        card_id: str,
        url: str | None = None,
        name: str | None = None,
        mime_type: str | None = None,
        set_cover: bool | None = None,
    ) -> TrelloAttachment:
        """Adds a URL attachment to a card.

        Args:
            card_id: The ID of the card.
            url: The URL to attach.
            name: Optional display name for the attachment.
            mime_type: Optional MIME type of the attachment.
            set_cover: Whether to use this attachment as the card cover.

        Returns:
            The created attachment object.
        """
        data: dict = {}
        if url is not None:
            data["url"] = url
        if name is not None:
            data["name"] = name
        if mime_type is not None:
            data["mimeType"] = mime_type
        if set_cover is not None:
            data["setCover"] = str(set_cover).lower()
        response = await self.client.POST_FORM(
            f"/cards/{card_id}/attachments",
            data=data,
        )
        return TrelloAttachment(**response)

    async def delete_attachment(self, card_id: str, attachment_id: str) -> Dict[str, Any]:
        """Deletes an attachment from a card.

        Args:
            card_id: The ID of the card.
            attachment_id: The ID of the attachment to delete.

        Returns:
            The response from the delete operation.
        """
        return await self.client.DELETE(
            f"/cards/{card_id}/attachments/{attachment_id}"
        )
