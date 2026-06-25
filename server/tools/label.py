"""
This module contains tools for managing Trello labels.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloLabel
from server.dtos.update_label import UpdateLabelPayload
from server.services.label import LabelService
from server.validators import ValidationService
from server.trello import client
from server.exceptions import TrelloMCPError

logger = logging.getLogger(__name__)

service = LabelService(client)
validator = ValidationService(client)


async def update_label(
    ctx: Context, label_id: str, payload: UpdateLabelPayload
) -> TrelloLabel:
    """Update a label's name or color.

    Args:
        label_id (str): The ID of the label.
        payload (UpdateLabelPayload): The new name and/or color.

    Returns:
        TrelloLabel: The updated label object.
    """
    try:
        logger.info(f"Updating label: {label_id}")
        
        # Convert payload to API parameters
        params = payload.to_api_params()
        
        if not params:
            error_msg = "No updates provided. Please specify name and/or color."
            logger.error(error_msg)
            await ctx.error(error_msg)
            raise ValueError(error_msg)
        
        result = await service.update_label(label_id, **params)
        logger.info(f"Successfully updated label: {label_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to update label: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to update label: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def delete_label(ctx: Context, label_id: str) -> dict:
    """Delete a label from its board.

    Args:
        label_id (str): The ID of the label to delete.

    Returns:
        dict: Confirmation of deletion.
    """
    try:
        logger.info(f"Deleting label: {label_id}")
        
        await service.delete_label(label_id)
        logger.info(f"Successfully deleted label: {label_id}")
        return {
            "success": True,
            "message": f"Label {label_id} deleted successfully"
        }
    except TrelloMCPError as e:
        error_msg = f"Failed to delete label: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to delete label: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_card_labels(ctx: Context, card_id: str) -> List[TrelloLabel]:
    """Retrieves all labels on a card.

    Args:
        card_id (str): The ID of the card.

    Returns:
        List[TrelloLabel]: A list of label objects.
    """
    try:
        logger.info(f"Getting labels for card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        result = await service.get_card_labels(card_id)
        logger.info(f"Successfully retrieved {len(result)} labels for card: {card_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get card labels: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get card labels: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def add_label_to_card(
    ctx: Context, card_id: str, label_id: str
) -> List[TrelloLabel]:
    """Add a label to a card.

    Args:
        card_id (str): The ID of the card.
        label_id (str): The ID of the label to add.

    Returns:
        List[TrelloLabel]: Updated list of labels on the card.
    """
    try:
        logger.info(f"Adding label {label_id} to card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        result = await service.add_label_to_card(card_id, label_id)
        logger.info(f"Successfully added label {label_id} to card: {card_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to add label to card: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to add label to card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def remove_label_from_card(
    ctx: Context, card_id: str, label_id: str
) -> dict:
    """Remove a label from a card.

    Args:
        card_id (str): The ID of the card.
        label_id (str): The ID of the label to remove.

    Returns:
        dict: Confirmation of removal.
    """
    try:
        logger.info(f"Removing label {label_id} from card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        await service.remove_label_from_card(card_id, label_id)
        logger.info(f"Successfully removed label {label_id} from card: {card_id}")
        return {
            "success": True,
            "message": f"Label {label_id} removed from card {card_id}"
        }
    except TrelloMCPError as e:
        error_msg = f"Failed to remove label from card: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to remove label from card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
