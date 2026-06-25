"""
This module contains tools for managing Trello lists.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloList
from server.services.list import ListService
from server.validators import ValidationService
from server.trello import client
from server.exceptions import TrelloMCPError

logger = logging.getLogger(__name__)

service = ListService(client)
validator = ValidationService(client)


# List Tools
async def get_list(ctx: Context, list_id: str) -> TrelloList:
    """Retrieves a specific list by its ID.

    Args:
        list_id (str): The ID of the list to retrieve.

    Returns:
        TrelloList: The list object containing list details.
    """
    try:
        logger.info(f"Getting list with ID: {list_id}")
        result = await service.get_list(list_id)
        logger.info(f"Successfully retrieved list: {list_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get list: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_lists(ctx: Context, board_id: str) -> List[TrelloList]:
    """Retrieves all lists on a given board.

    Args:
        board_id (str): The ID of the board whose lists to retrieve.

    Returns:
        List[TrelloList]: A list of list objects.
    """
    try:
        logger.info(f"Getting lists for board: {board_id}")
        # Validate board exists
        await validator.validate_board_exists(board_id)
        result = await service.get_lists(board_id)
        logger.info(f"Successfully retrieved {len(result)} lists for board: {board_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get lists: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get lists: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def create_list(
    ctx: Context, board_id: str, name: str, pos: str = "bottom"
) -> TrelloList:
    """Creates a new list on a given board.

    Args:
        board_id (str): The ID of the board to create the list in.
        name (str): The name of the new list.
        pos (str, optional): The position of the new list. Can be "top" or "bottom". Defaults to "bottom".

    Returns:
        TrelloList: The newly created list object.
    """
    try:
        logger.info(f"Creating list '{name}' in board: {board_id}")
        # Validate board exists
        await validator.validate_board_exists(board_id)
        # Validate name is not empty
        if not name or not name.strip():
            raise TrelloMCPError("List name cannot be empty")
        result = await service.create_list(board_id, name, pos)
        logger.info(f"Successfully created list '{name}' in board: {board_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to create list: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to create list: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def update_list(ctx: Context, list_id: str, name: str) -> TrelloList:
    """Updates the name of a list.

    Args:
        list_id (str): The ID of the list to update.
        name (str): The new name for the list.

    Returns:
        TrelloList: The updated list object.
    """
    try:
        logger.info(f"Updating list {list_id} with new name: {name}")
        # Validate list exists
        await validator.validate_list_exists(list_id)
        # Validate name is not empty
        if not name or not name.strip():
            raise TrelloMCPError("List name cannot be empty")
        result = await service.update_list(list_id, name)
        logger.info(f"Successfully updated list: {list_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to update list: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to update list: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def delete_list(ctx: Context, list_id: str) -> TrelloList:
    """Archives a list.

    Args:
        list_id (str): The ID of the list to close.

    Returns:
        TrelloList: The archived list object.
    """
    try:
        logger.info(f"Archiving list: {list_id}")
        # Validate list exists
        await validator.validate_list_exists(list_id)
        result = await service.delete_list(list_id)
        logger.info(f"Successfully archived list: {list_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to delete list: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to delete list: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
