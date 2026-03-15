"""
This module contains tools for managing Trello card comments and attachments.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloAttachment, TrelloComment
from server.services.comment import CommentService
from server.trello import client

logger = logging.getLogger(__name__)

service = CommentService(client)


async def get_comments(ctx: Context, card_id: str) -> List[TrelloComment]:
    """Retrieves all comments on a card.

    Args:
        card_id (str): The ID of the card to get comments for.

    Returns:
        List[TrelloComment]: A list of comment objects, each containing the comment
            text in data.text, the author in memberCreator, and the date.
    """
    try:
        logger.info(f"Getting comments for card: {card_id}")
        result = await service.get_comments(card_id)
        logger.info(f"Successfully retrieved {len(result)} comments for card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get comments: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def add_comment(ctx: Context, card_id: str, text: str) -> TrelloComment:
    """Adds a comment to a card. Supports Trello markdown formatting and @mentions.

    Args:
        card_id (str): The ID of the card to comment on.
        text (str): The comment text. Supports markdown formatting and @mentions
            (use @username to mention a board member).

    Returns:
        TrelloComment: The created comment object.
    """
    try:
        logger.info(f"Adding comment to card: {card_id}")
        result = await service.add_comment(card_id, text)
        logger.info(f"Successfully added comment to card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to add comment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def update_comment(
    ctx: Context, card_id: str, action_id: str, text: str
) -> TrelloComment:
    """Updates an existing comment on a card.

    Args:
        card_id (str): The ID of the card the comment belongs to.
        action_id (str): The ID of the comment action to update (from get_comments).
        text (str): The new comment text.

    Returns:
        TrelloComment: The updated comment object.
    """
    try:
        logger.info(f"Updating comment {action_id} on card: {card_id}")
        result = await service.update_comment(card_id, action_id, text)
        logger.info(f"Successfully updated comment {action_id} on card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to update comment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def delete_comment(ctx: Context, card_id: str, action_id: str) -> dict:
    """Deletes a comment from a card.

    Args:
        card_id (str): The ID of the card the comment belongs to.
        action_id (str): The ID of the comment action to delete (from get_comments).

    Returns:
        dict: The response from the delete operation.
    """
    try:
        logger.info(f"Deleting comment {action_id} from card: {card_id}")
        result = await service.delete_comment(card_id, action_id)
        logger.info(f"Successfully deleted comment {action_id} from card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to delete comment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_attachments(ctx: Context, card_id: str) -> List[TrelloAttachment]:
    """Retrieves all attachments on a card.

    Args:
        card_id (str): The ID of the card to get attachments for.

    Returns:
        List[TrelloAttachment]: A list of attachment objects.
    """
    try:
        logger.info(f"Getting attachments for card: {card_id}")
        result = await service.get_attachments(card_id)
        logger.info(f"Successfully retrieved {len(result)} attachments for card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get attachments: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def add_attachment(
    ctx: Context,
    card_id: str,
    url: str,
    name: str | None = None,
    mime_type: str | None = None,
    set_cover: bool | None = None,
) -> TrelloAttachment:
    """Adds a URL attachment to a card. Use this to attach links to external
    resources like GitHub PRs, documents, images, or any other URL.

    Args:
        card_id (str): The ID of the card to attach to.
        url (str): The URL to attach.
        name (str, optional): Display name for the attachment. Defaults to the URL.
        mime_type (str, optional): MIME type of the resource (e.g. "image/png").
        set_cover (bool, optional): Whether to use this attachment as the card cover image.

    Returns:
        TrelloAttachment: The created attachment object.
    """
    try:
        logger.info(f"Adding attachment to card: {card_id}")
        result = await service.add_attachment(
            card_id, url=url, name=name, mime_type=mime_type, set_cover=set_cover
        )
        logger.info(f"Successfully added attachment to card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to add attachment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def delete_attachment(ctx: Context, card_id: str, attachment_id: str) -> dict:
    """Deletes an attachment from a card.

    Args:
        card_id (str): The ID of the card the attachment belongs to.
        attachment_id (str): The ID of the attachment to delete (from get_attachments).

    Returns:
        dict: The response from the delete operation.
    """
    try:
        logger.info(f"Deleting attachment {attachment_id} from card: {card_id}")
        result = await service.delete_attachment(card_id, attachment_id)
        logger.info(f"Successfully deleted attachment {attachment_id} from card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to delete attachment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
