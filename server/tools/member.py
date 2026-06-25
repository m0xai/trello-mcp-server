"""
This module contains tools for managing Trello members.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloMember
from server.dtos.add_board_member import AddBoardMemberPayload
from server.dtos.update_board_member import UpdateBoardMemberPayload
from server.services.member import MemberService
from server.validators import ValidationService
from server.trello import client
from server.exceptions import TrelloMCPError

logger = logging.getLogger(__name__)

service = MemberService(client)
validator = ValidationService(client)


async def get_board_members(ctx: Context, board_id: str) -> List[TrelloMember]:
    """Retrieves all members of a board.

    Args:
        board_id (str): The ID of the board.

    Returns:
        List[TrelloMember]: A list of member objects.
    """
    try:
        logger.info(f"Getting members for board: {board_id}")
        
        # Validate board exists
        await validator.validate_board_exists(board_id)
        
        result = await service.get_board_members(board_id)
        logger.info(f"Successfully retrieved {len(result)} members for board: {board_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get board members: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get board members: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def add_board_member(
    ctx: Context, board_id: str, payload: AddBoardMemberPayload
) -> TrelloMember:
    """Add a member to a board.

    Args:
        board_id (str): The ID of the board.
        payload (AddBoardMemberPayload): The member details (email, type).

    Returns:
        TrelloMember: The added member object.
    """
    try:
        logger.info(f"Adding member {payload.email} to board: {board_id}")
        
        # Validate board exists
        await validator.validate_board_exists(board_id)
        
        # Convert payload to API parameters
        params = payload.to_api_params()
        
        result = await service.add_board_member(board_id, **params)
        logger.info(f"Successfully added member {payload.email} to board: {board_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to add board member: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to add board member: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def update_board_member(
    ctx: Context, board_id: str, member_id: str, payload: UpdateBoardMemberPayload
) -> TrelloMember:
    """Update a board member's role.

    Args:
        board_id (str): The ID of the board.
        member_id (str): The ID of the member.
        payload (UpdateBoardMemberPayload): The new member type.

    Returns:
        TrelloMember: The updated member object.
    """
    try:
        logger.info(f"Updating member {member_id} on board: {board_id}")
        
        # Validate board exists
        await validator.validate_board_exists(board_id)
        
        # Convert payload to API parameters
        params = payload.to_api_params()
        
        result = await service.update_board_member(board_id, member_id, **params)
        logger.info(f"Successfully updated member {member_id} on board: {board_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to update board member: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to update board member: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def remove_board_member(ctx: Context, board_id: str, member_id: str) -> dict:
    """Remove a member from a board.

    Args:
        board_id (str): The ID of the board.
        member_id (str): The ID of the member to remove.

    Returns:
        dict: Confirmation of removal.
    """
    try:
        logger.info(f"Removing member {member_id} from board: {board_id}")
        
        # Validate board exists
        await validator.validate_board_exists(board_id)
        
        await service.remove_board_member(board_id, member_id)
        logger.info(f"Successfully removed member {member_id} from board: {board_id}")
        return {
            "success": True,
            "message": f"Member {member_id} removed from board {board_id}"
        }
    except TrelloMCPError as e:
        error_msg = f"Failed to remove board member: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to remove board member: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_workspace_members(ctx: Context, workspace_id: str) -> List[TrelloMember]:
    """Retrieves all members of a workspace/organization.

    Args:
        workspace_id (str): The ID of the workspace.

    Returns:
        List[TrelloMember]: A list of member objects.
    """
    try:
        logger.info(f"Getting members for workspace: {workspace_id}")
        
        # Validate workspace exists
        await validator.validate_organization_exists(workspace_id)
        
        result = await service.get_workspace_members(workspace_id)
        logger.info(
            f"Successfully retrieved {len(result)} members for workspace: {workspace_id}"
        )
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get workspace members: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get workspace members: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_member(ctx: Context, member_id: str = "me") -> TrelloMember:
    """Retrieves a specific member by ID.

    Args:
        member_id (str): The ID of the member (or "me" for authenticated user).

    Returns:
        TrelloMember: The member object.
    """
    try:
        logger.info(f"Getting member: {member_id}")
        
        result = await service.get_member(member_id)
        logger.info(f"Successfully retrieved member: {member_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get member: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get member: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_card_members(ctx: Context, card_id: str) -> List[TrelloMember]:
    """Retrieves all members assigned to a card.

    Args:
        card_id (str): The ID of the card.

    Returns:
        List[TrelloMember]: A list of member objects.
    """
    try:
        logger.info(f"Getting members for card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        result = await service.get_card_members(card_id)
        logger.info(f"Successfully retrieved {len(result)} members for card: {card_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get card members: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get card members: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def add_card_member(ctx: Context, card_id: str, member_id: str) -> List[TrelloMember]:
    """Add a member to a card.

    Args:
        card_id (str): The ID of the card.
        member_id (str): The ID of the member to add.

    Returns:
        List[TrelloMember]: Updated list of card members.
    """
    try:
        logger.info(f"Adding member {member_id} to card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        result = await service.add_card_member(card_id, member_id)
        logger.info(f"Successfully added member {member_id} to card: {card_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to add card member: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to add card member: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def remove_card_member(ctx: Context, card_id: str, member_id: str) -> dict:
    """Remove a member from a card.

    Args:
        card_id (str): The ID of the card.
        member_id (str): The ID of the member to remove.

    Returns:
        dict: Confirmation of removal.
    """
    try:
        logger.info(f"Removing member {member_id} from card: {card_id}")
        
        # Validate card exists
        await validator.validate_card_exists(card_id)
        
        await service.remove_card_member(card_id, member_id)
        logger.info(f"Successfully removed member {member_id} from card: {card_id}")
        return {
            "success": True,
            "message": f"Member {member_id} removed from card {card_id}"
        }
    except TrelloMCPError as e:
        error_msg = f"Failed to remove card member: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to remove card member: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
