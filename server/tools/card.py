"""
This module contains tools for managing Trello cards.
"""

import logging
from typing import Any, Dict, List

from mcp.server.fastmcp import Context

from server.models import TrelloCard
from server.services.card import CardService
from server.trello import client
from server.dtos.update_card import UpdateCardPayload
from server.dtos.create_card import CreateCardPayload

logger = logging.getLogger(__name__)

service = CardService(client)


async def get_card(ctx: Context, card_id: str) -> TrelloCard:
    """Retrieves a specific card by its ID.

    Args:
        card_id (str): The ID of the card to retrieve.

    Returns:
        TrelloCard: The card object containing card details.
    """
    try:
        logger.info(f"Getting card with ID: {card_id}")
        result = await service.get_card(card_id)
        logger.info(f"Successfully retrieved card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_cards(
    ctx: Context,
    list_id: str,
    member_id: str | None = None,
    label_id: str | None = None,
) -> List[TrelloCard]:
    """Retrieves all cards in a given list with optional filtering.

    Args:
        list_id (str): The ID of the list whose cards to retrieve.
        member_id (str, optional): Filter to cards assigned to this member ID.
        label_id (str, optional): Filter to cards that have this label ID.

    Returns:
        List[TrelloCard]: A list of card objects.
    """
    try:
        logger.info(f"Getting cards for list: {list_id}")
        result = await service.get_cards(list_id, member_id=member_id, label_id=label_id)
        logger.info(f"Successfully retrieved {len(result)} cards for list: {list_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get cards: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def create_card(ctx: Context, payload: CreateCardPayload) -> TrelloCard:
    """Creates a new card in a given list.

    Args:
        list_id (str): The ID of the list to create the card in.
        name (str): The name of the new card.
        desc (str, optional): The description of the new card. Defaults to None.

    Returns:
        TrelloCard: The newly created card object.
    """
    try:
        logger.info(f"Creating card in list {payload.idList} with name: {payload.name}")
        result = await service.create_card(**payload.model_dump(exclude_unset=True))
        logger.info(f"Successfully created card in list: {payload.idList}")
        return result
    except Exception as e:
        error_msg = f"Failed to create card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def update_card(
    ctx: Context, card_id: str, payload: UpdateCardPayload
) -> TrelloCard:
    """Updates a card's attributes.

    Args:
        card_id (str): The ID of the card to update.
        **kwargs: Keyword arguments representing the attributes to update on the card.

    Returns:
        TrelloCard: The updated card object.
    """
    try:
        logger.info(f"Updating card: {card_id} with payload: {payload}")
        result = await service.update_card(
            card_id, **payload.model_dump(exclude_unset=True)
        )
        logger.info(f"Successfully updated card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to update card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def delete_card(ctx: Context, card_id: str) -> dict:
    """Deletes a card permanently.

    Args:
        card_id (str): The ID of the card to delete.

    Returns:
        dict: The response from the delete operation.
    """
    try:
        logger.info(f"Deleting card: {card_id}")
        result = await service.delete_card(card_id)
        logger.info(f"Successfully deleted card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to delete card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def archive_card(ctx: Context, card_id: str) -> TrelloCard:
    """Archives a card (closes it without deleting). The card remains recoverable.

    Args:
        card_id (str): The ID of the card to archive.

    Returns:
        TrelloCard: The archived card object.
    """
    try:
        logger.info(f"Archiving card: {card_id}")
        result = await service.archive_card(card_id)
        logger.info(f"Successfully archived card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to archive card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_card_comments(ctx: Context, card_id: str) -> List[Dict[str, Any]]:
    """Retrieves all comments on a card.

    Args:
        card_id (str): The ID of the card whose comments to retrieve.

    Returns:
        List[Dict[str, Any]]: A list of comment action objects with id, date, memberCreator, and text.
    """
    try:
        logger.info(f"Getting comments for card: {card_id}")
        result = await service.get_card_comments(card_id)
        logger.info(f"Successfully retrieved {len(result)} comments for card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get card comments: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def add_comment_to_card(ctx: Context, card_id: str, text: str) -> Dict[str, Any]:
    """Adds a comment to a card.

    Args:
        card_id (str): The ID of the card to comment on.
        text (str): The comment text.

    Returns:
        Dict[str, Any]: The created comment action object.
    """
    try:
        logger.info(f"Adding comment to card: {card_id}")
        result = await service.add_comment_to_card(card_id, text)
        logger.info(f"Successfully added comment to card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to add comment to card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def add_member_to_card(ctx: Context, card_id: str, member_id: str) -> List[str]:
    """Adds a member to a card.

    Args:
        card_id (str): The ID of the card.
        member_id (str): The ID of the member to add.

    Returns:
        List[str]: The updated list of member IDs assigned to the card.
    """
    try:
        logger.info(f"Adding member {member_id} to card: {card_id}")
        result = await service.add_member_to_card(card_id, member_id)
        logger.info(f"Successfully added member {member_id} to card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to add member to card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def remove_member_from_card(ctx: Context, card_id: str, member_id: str) -> Dict[str, Any]:
    """Removes a member from a card.

    Args:
        card_id (str): The ID of the card.
        member_id (str): The ID of the member to remove.

    Returns:
        Dict[str, Any]: The response from the remove operation.
    """
    try:
        logger.info(f"Removing member {member_id} from card: {card_id}")
        result = await service.remove_member_from_card(card_id, member_id)
        logger.info(f"Successfully removed member {member_id} from card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to remove member from card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def search_cards(
    ctx: Context, query: str, board_id: str | None = None
) -> List[TrelloCard]:
    """Searches for cards matching a query across all boards or within a specific board.

    Args:
        query (str): The search query string.
        board_id (str, optional): Limit results to this board ID.

    Returns:
        List[TrelloCard]: A list of matching card objects.
    """
    try:
        logger.info(f"Searching cards with query: {query}")
        result = await service.search_cards(query, board_id=board_id)
        logger.info(f"Successfully found {len(result)} cards matching query: {query}")
        return result
    except Exception as e:
        error_msg = f"Failed to search cards: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
