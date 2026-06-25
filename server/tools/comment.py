"""
This module contains tools for managing Trello comments and actions.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloAction
from server.dtos.add_comment import AddCommentPayload
from server.dtos.update_comment import UpdateCommentPayload
from server.services.comment import CommentService
from server.validators import ValidationService
from server.trello import client
from server.exceptions import TrelloMCPError

logger = logging.getLogger(__name__)

service = CommentService(client)
validator = ValidationService(client)


async def get_card_comments(ctx: Context, card_id: str) -> List[TrelloAction]:
    """Retrieves all comments on a card.

    Args:
        card_id (str): The ID of the card.

    Returns:
        List[TrelloAction]: A list of comment actions.
    """
    try:
        logger.info(f"Getting comments for card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        result = await service.get_card_comments(card_id)
        logger.info(f"Successfully retrieved {len(result)} comments for card: {card_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get card comments: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get card comments: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_card_actions(
    ctx: Context, card_id: str, filter: str = "all", limit: int = 50
) -> List[TrelloAction]:
    """Retrieves actions/activity on a card.

    Args:
        card_id (str): The ID of the card.
        filter (str): Filter for action types (default: "all").
        limit (int): Maximum number of actions to return (default: 50, max: 1000).

    Returns:
        List[TrelloAction]: A list of action objects.
    """
    try:
        logger.info(f"Getting actions for card: {card_id} with filter: {filter}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        # Validate limit
        if limit > 1000:
            limit = 1000
            logger.warning(f"Limit capped at 1000 (requested: {limit})")
        
        result = await service.get_card_actions(card_id, filter, limit)
        logger.info(f"Successfully retrieved {len(result)} actions for card: {card_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get card actions: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get card actions: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def add_comment(
    ctx: Context, card_id: str, payload: AddCommentPayload
) -> TrelloAction:
    """Add a comment to a card.

    Args:
        card_id (str): The ID of the card.
        payload (AddCommentPayload): The comment text.

    Returns:
        TrelloAction: The created comment action.
    """
    try:
        logger.info(f"Adding comment to card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        # Convert payload to API parameters
        params = payload.to_api_params()
        
        result = await service.add_comment(card_id, **params)
        logger.info(f"Successfully added comment to card: {card_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to add comment: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to add comment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def update_comment(
    ctx: Context, action_id: str, payload: UpdateCommentPayload
) -> TrelloAction:
    """Update a comment.

    Args:
        action_id (str): The ID of the comment action.
        payload (UpdateCommentPayload): The new comment text.

    Returns:
        TrelloAction: The updated comment action.
    """
    try:
        logger.info(f"Updating comment: {action_id}")
        
        # Convert payload to API parameters
        params = payload.to_api_params()
        
        result = await service.update_comment(action_id, **params)
        logger.info(f"Successfully updated comment: {action_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to update comment: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to update comment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def delete_comment(ctx: Context, action_id: str) -> dict:
    """Delete a comment.

    Args:
        action_id (str): The ID of the comment action to delete.

    Returns:
        dict: Confirmation of deletion.
    """
    try:
        logger.info(f"Deleting comment: {action_id}")
        
        await service.delete_comment(action_id)
        logger.info(f"Successfully deleted comment: {action_id}")
        return {
            "success": True,
            "message": f"Comment {action_id} deleted successfully"
        }
    except TrelloMCPError as e:
        error_msg = f"Failed to delete comment: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to delete comment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_board_actions(
    ctx: Context, board_id: str, filter: str = "all", limit: int = 50
) -> List[TrelloAction]:
    """Retrieves actions/activity on a board.

    Args:
        board_id (str): The ID of the board.
        filter (str): Filter for action types (default: "all").
        limit (int): Maximum number of actions to return (default: 50, max: 1000).

    Returns:
        List[TrelloAction]: A list of action objects.
    """
    try:
        logger.info(f"Getting actions for board: {board_id} with filter: {filter}")
        
        # Validate board exists
        await validator.validate_board_exists(board_id)
        
        # Validate limit
        if limit > 1000:
            limit = 1000
            logger.warning(f"Limit capped at 1000 (requested: {limit})")
        
        result = await service.get_board_actions(board_id, filter, limit)
        logger.info(f"Successfully retrieved {len(result)} actions for board: {board_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get board actions: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get board actions: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
