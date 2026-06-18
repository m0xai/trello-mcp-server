"""
This module contains tools for managing Trello members.
"""

import logging

from mcp.server.fastmcp import Context

from server.models import TrelloMember
from server.services.member import MemberService
from server.trello import client

logger = logging.getLogger(__name__)

service = MemberService(client)


async def get_member(ctx: Context, member_id: str) -> TrelloMember:
    """Retrieves a member by their ID or username.

    Args:
        member_id (str): The Trello member ID or username to look up.

    Returns:
        TrelloMember: The member object containing id, fullName, and username.
    """
    try:
        logger.info(f"Getting member: {member_id}")
        result = await service.get_member(member_id)
        logger.info(f"Successfully retrieved member: {member_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get member: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
