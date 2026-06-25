"""
from server.validators import ValidationService
MCP tools for export, import, and template operations.
"""

import json
from mcp.server.fastmcp import Context
from server.trello import client
nservice = ExportService(client)
validator = ValidationService(client)
from server.services.export import ExportService
from server.validators.validation_service import ValidationService



async def export_board(ctx: Context, board_id: str) -> str:
    """
    Export a complete board with all data (cards, lists, members, labels, checklists, custom fields).
    
    This creates a comprehensive JSON export that can be used for:
    - Backup and restore
    - Board templates
    - Data analysis
    - Migration to other systems
    
    Args:
        board_id: The ID of the board to export
        
    Returns:
        JSON string containing complete board data
    """
    client = client
    # Using global validator
    # Using global service
    
    # Validate board exists
    await validator.validate_board_exists(board_id)
    
    # Export board
    board_data = service.export_board(board_id)
    
    cards_count = len(board_data.get("cards", []))
    lists_count = len(board_data.get("lists", []))
    members_count = len(board_data.get("members", []))
    
    return f"Exported board '{board_data.get('name')}' with {lists_count} lists, {cards_count} cards, {members_count} members. Full data: {json.dumps(board_data)}"



async def list_organization_exports(ctx: Context, organization_id: str) -> str:
    """
    List all exports for an organization/workspace.
    
    Args:
        organization_id: The ID of the organization
        
    Returns:
        JSON string containing list of exports
    """
    client = client
    # Using global service
    
    # List exports
    exports = service.list_organization_exports(organization_id)
    
    return f"Found {len(exports)} export(s) for organization: {json.dumps(exports)}"



async def create_organization_export(
    ctx: Context,
    organization_id: str,
    include_attachments: bool = True
) -> str:
    """
    Create a new export for an organization/workspace.
    
    This generates a comprehensive export of all boards in the organization.
    The export is processed asynchronously and a download URL is provided when ready.
    
    Args:
        organization_id: The ID of the organization
        include_attachments: Whether to include attachments in the export (default True)
        
    Returns:
        JSON string containing export status and information
    """
    client = client
    # Using global service
    
    # Create export
    export_data = service.create_organization_export(organization_id, include_attachments)
    
    return f"Created export for organization {organization_id}. Export ID: {export_data.get('id')}. Status: {export_data.get('status')}. Data: {json.dumps(export_data)}"



async def create_board_from_template(
    ctx: Context,
    template_board_id: str,
    name: str,
    organization_id: str = None
) -> str:
    """
    Create a new board using an existing board as a template.
    
    This copies the structure (lists, labels, custom fields) from the template board
    to create a new board. Cards are not copied by default.
    
    Args:
        template_board_id: The ID of the board to use as template
        name: Name for the new board
        organization_id: Optional organization ID to create board in
        
    Returns:
        JSON string containing the created board information
    """
    client = client
    # Using global validator
    
    # Validate template board exists
    await validator.validate_board_exists(template_board_id)
    
    # Create board from template
    params = {
        "name": name,
        "idBoardSource": template_board_id,
        "keepFromSource": "cards"  # This actually means DON'T keep cards in Trello API
    }
    
    if organization_id:
        params["idOrganization"] = organization_id
    
    response = client.post("/boards", params=params)
    
    return f"Created board '{response['name']}' (ID: {response['id']}) from template {template_board_id}"
