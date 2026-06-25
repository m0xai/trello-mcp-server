"""
This module contains tools for managing Trello workspaces/organizations.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloBoard, TrelloOrganization
from server.dtos.create_workspace import CreateWorkspacePayload
from server.dtos.update_workspace import UpdateWorkspacePayload
from server.services.workspace import WorkspaceService
from server.validators import ValidationService
from server.trello import client
from server.exceptions import TrelloMCPError

logger = logging.getLogger(__name__)

service = WorkspaceService(client)
validator = ValidationService(client)


async def get_workspaces(ctx: Context) -> List[TrelloOrganization]:
    """Retrieves all workspaces/organizations for the authenticated user.

    Returns:
        List[TrelloOrganization]: A list of workspace objects.
    """
    try:
        logger.info("Getting all workspaces")
        result = await service.get_workspaces()
        logger.info(f"Successfully retrieved {len(result)} workspaces")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get workspaces: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get workspaces: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_workspace(ctx: Context, workspace_id: str) -> TrelloOrganization:
    """Retrieves a specific workspace/organization by its ID.

    Args:
        workspace_id (str): The ID of the workspace to retrieve.

    Returns:
        TrelloOrganization: The workspace object containing workspace details.
    """
    try:
        logger.info(f"Getting workspace with ID: {workspace_id}")
        
        # Validate workspace exists
        await validator.validate_organization_exists(workspace_id)
        
        result = await service.get_workspace(workspace_id)
        logger.info(f"Successfully retrieved workspace: {workspace_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get workspace: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get workspace: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_workspace_boards(
    ctx: Context, workspace_id: str, filter_value: str = "all"
) -> List[TrelloBoard]:
    """Retrieves all boards in a workspace/organization.

    Args:
        workspace_id (str): The ID of the workspace whose boards to retrieve.
        filter_value (str): Filter for boards. Options: all, open, closed, members,
                          organization, public. Defaults to "all".

    Returns:
        List[TrelloBoard]: A list of board objects in the workspace.
    """
    try:
        logger.info(f"Getting boards for workspace: {workspace_id} with filter: {filter_value}")
        
        # Validate workspace exists
        await validator.validate_organization_exists(workspace_id)
        
        # Validate filter value
        validator.validate_board_filter(filter_value)
        
        result = await service.get_workspace_boards(workspace_id, filter_value)
        logger.info(
            f"Successfully retrieved {len(result)} boards for workspace: {workspace_id}"
        )
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to get workspace boards: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to get workspace boards: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def create_workspace(
    ctx: Context, payload: CreateWorkspacePayload
) -> TrelloOrganization:
    """Create a new workspace/organization.

    Args:
        payload (CreateWorkspacePayload): The workspace creation payload containing display name,
                                         description, short name, and website.

    Returns:
        TrelloOrganization: The newly created workspace object.
    """
    try:
        logger.info(f"Creating workspace: {payload.display_name}")
        
        # Convert payload to API parameters
        params = payload.to_api_params()
        
        result = await service.create_workspace(**params)
        logger.info(f"Successfully created workspace: {result.id} - {result.displayName}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to create workspace: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to create workspace: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def update_workspace(
    ctx: Context, workspace_id: str, payload: UpdateWorkspacePayload
) -> TrelloOrganization:
    """Update an existing workspace/organization.

    Args:
        workspace_id (str): The ID of the workspace to update.
        payload (UpdateWorkspacePayload): The workspace update payload containing fields to update.

    Returns:
        TrelloOrganization: The updated workspace object.
    """
    try:
        logger.info(f"Updating workspace: {workspace_id}")
        
        # Validate workspace exists
        await validator.validate_organization_exists(workspace_id)
        
        # Convert payload to API parameters
        params = payload.to_api_params()
        
        result = await service.update_workspace(workspace_id, **params)
        logger.info(f"Successfully updated workspace: {workspace_id}")
        return result
    except TrelloMCPError as e:
        error_msg = f"Failed to update workspace: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to update workspace: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def delete_workspace(ctx: Context, workspace_id: str) -> dict:
    """Delete a workspace/organization permanently.

    Args:
        workspace_id (str): The ID of the workspace to delete.

    Returns:
        dict: Confirmation of deletion.
    """
    try:
        logger.info(f"Deleting workspace: {workspace_id}")
        
        # Validate workspace exists
        await validator.validate_organization_exists(workspace_id)
        
        # Note: Trello API requires admin permissions to delete a workspace
        # The API will return 403 if user doesn't have permission
        
        result = await service.delete_workspace(workspace_id)
        logger.info(f"Successfully deleted workspace: {workspace_id}")
        return {"success": True, "message": f"Workspace {workspace_id} has been permanently deleted"}
    except TrelloMCPError as e:
        error_msg = f"Failed to delete workspace: {e.message}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Failed to delete workspace: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
