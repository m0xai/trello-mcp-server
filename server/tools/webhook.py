"""
This module contains tools for managing Trello webhooks.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloWebhook
from server.dtos.create_webhook import CreateWebhookPayload
from server.dtos.update_webhook import UpdateWebhookPayload
from server.services.webhook import WebhookService
from server.validators import ValidationService
from server.trello import client
from server.exceptions import TrelloMCPError

logger = logging.getLogger(__name__)

service = WebhookService(client)
validator = ValidationService(client)


async def create_webhook(ctx: Context, payload: CreateWebhookPayload) -> TrelloWebhook:
    """Create a new webhook.

    Args:
        payload (CreateWebhookPayload): Webhook configuration (callbackURL, idModel, etc.).

    Returns:
        TrelloWebhook: The created webhook object.
    """
    try:
        logger.info(f"Creating webhook for model: {payload.id_model}")
        
        # Convert payload to API parameters
        params = payload.to_api_params()
        
        result = await service.create_webhook(**params)
        logger.info(f"Successfully created webhook: {result.id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to create webhook: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to create webhook: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_webhook(ctx: Context, webhook_id: str) -> TrelloWebhook:
    """Retrieves a specific webhook by ID.

    Args:
        webhook_id (str): The ID of the webhook.

    Returns:
        TrelloWebhook: The webhook object.
    """
    try:
        logger.info(f"Getting webhook: {webhook_id}")
        
        result = await service.get_webhook(webhook_id)
        logger.info(f"Successfully retrieved webhook: {webhook_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get webhook: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get webhook: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def list_webhooks(ctx: Context, token: str) -> List[TrelloWebhook]:
    """Retrieves all webhooks for a token.

    Args:
        token (str): The API token (use the token from environment or "me").

    Returns:
        List[TrelloWebhook]: A list of webhook objects.
    """
    try:
        logger.info(f"Listing webhooks for token")
        
        result = await service.list_webhooks(token)
        logger.info(f"Successfully retrieved {len(result)} webhooks")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to list webhooks: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to list webhooks: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def update_webhook(
    ctx: Context, webhook_id: str, payload: UpdateWebhookPayload
) -> TrelloWebhook:
    """Update a webhook.

    Args:
        webhook_id (str): The ID of the webhook.
        payload (UpdateWebhookPayload): The webhook updates.

    Returns:
        TrelloWebhook: The updated webhook object.
    """
    try:
        logger.info(f"Updating webhook: {webhook_id}")
        
        # Convert payload to API parameters
        params = payload.to_api_params()
        
        if not params:
            error_msg = "No updates provided. Please specify callbackURL, description, and/or active status."
            logger.error(error_msg)
            await ctx.error(error_msg)
            raise ValueError(error_msg)
        
        result = await service.update_webhook(webhook_id, **params)
        logger.info(f"Successfully updated webhook: {webhook_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to update webhook: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to update webhook: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def delete_webhook(ctx: Context, webhook_id: str) -> dict:
    """Delete a webhook.

    Args:
        webhook_id (str): The ID of the webhook to delete.

    Returns:
        dict: Confirmation of deletion.
    """
    try:
        logger.info(f"Deleting webhook: {webhook_id}")
        
        await service.delete_webhook(webhook_id)
        logger.info(f"Successfully deleted webhook: {webhook_id}")
        return {
            "success": True,
            "message": f"Webhook {webhook_id} deleted successfully"
        }
    except TrelloMCPError as e:
        error_msg = f"Failed to delete webhook: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to delete webhook: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
