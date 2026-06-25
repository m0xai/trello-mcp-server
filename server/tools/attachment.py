"""
This module contains tools for managing Trello card attachments.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloAttachment
from server.dtos.attach_url import AttachUrlPayload
from server.services.attachment import AttachmentService
from server.validators import ValidationService
from server.trello import client
from server.exceptions import TrelloMCPError

logger = logging.getLogger(__name__)

service = AttachmentService(client)
validator = ValidationService(client)


async def get_card_attachments(ctx: Context, card_id: str) -> List[TrelloAttachment]:
    """Retrieves all attachments on a card.

    Args:
        card_id (str): The ID of the card.

    Returns:
        List[TrelloAttachment]: A list of attachment objects.
    """
    try:
        logger.info(f"Getting attachments for card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        result = await service.get_card_attachments(card_id)
        logger.info(
            f"Successfully retrieved {len(result)} attachments for card: {card_id}"
        )
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get card attachments: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get card attachments: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def attach_url(
    ctx: Context, card_id: str, payload: AttachUrlPayload
) -> TrelloAttachment:
    """Attach a URL to a card.

    Args:
        card_id (str): The ID of the card.
        payload (AttachUrlPayload): The URL and optional name.

    Returns:
        TrelloAttachment: The created attachment object.
    """
    try:
        logger.info(f"Attaching URL to card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        # Convert payload to API parameters
        params = payload.to_api_params()
        
        result = await service.attach_url(card_id, **params)
        logger.info(f"Successfully attached URL to card: {card_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to attach URL: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to attach URL: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def delete_attachment(
    ctx: Context, card_id: str, attachment_id: str
) -> dict:
    """Delete an attachment from a card.

    Args:
        card_id (str): The ID of the card.
        attachment_id (str): The ID of the attachment to delete.

    Returns:
        dict: Confirmation of deletion.
    """
    try:
        logger.info(f"Deleting attachment {attachment_id} from card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        await service.delete_attachment(card_id, attachment_id)
        logger.info(
            f"Successfully deleted attachment {attachment_id} from card: {card_id}"
        )
        return {
            "success": True,
            "message": f"Attachment {attachment_id} deleted from card {card_id}"
        }
    except TrelloMCPError as e:
        error_msg = f"Failed to delete attachment: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to delete attachment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def set_attachment_as_cover(
    ctx: Context, card_id: str, attachment_id: str
) -> dict:
    """Set an attachment as the card cover.

    Args:
        card_id (str): The ID of the card.
        attachment_id (str): The ID of the attachment.

    Returns:
        dict: Confirmation of update.
    """
    try:
        logger.info(f"Setting attachment {attachment_id} as cover for card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        await service.set_attachment_as_cover(card_id, attachment_id)
        logger.info(
            f"Successfully set attachment {attachment_id} as cover for card: {card_id}"
        )
        return {
            "success": True,
            "message": f"Attachment {attachment_id} set as cover for card {card_id}"
        }
    except TrelloMCPError as e:
        error_msg = f"Failed to set attachment as cover: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to set attachment as cover: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
