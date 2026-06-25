"""
MCP tools for search operations.
"""

import json
from mcp.server.fastmcp import Context
from server.trello import client
from server.validators import ValidationService

service = SearchService(client)
validator = ValidationService(client)
from server.services.search import SearchService



async def search_trello(
    ctx: Context,
    query: str,
    board_ids: str = None,
    organization_ids: str = None,
    model_types: str = None,
    partial: bool = False
) -> str:
    """
    Search across Trello resources (cards, boards, members, organizations).
    
    Supports advanced query syntax:
    - @member: Filter by assigned member
    - #label: Filter by label
    - due:day/week/month: Filter by due date
    - is:open/archived: Filter by status
    - has:attachments/members: Filter by presence
    
    Args:
        query: Search query string
        board_ids: Comma-separated list of board IDs to limit search
        organization_ids: Comma-separated list of organization IDs to limit search
        model_types: Comma-separated list of types to search (cards, boards, members, organizations)
        partial: Enable partial matching (default False)
        
    Returns:
        JSON string containing search results grouped by type
    """
    client = client
    # Using global service
    
    # Perform search
    results = service.search(
        query=query,
        id_boards=board_ids,
        id_organizations=organization_ids,
        model_types=model_types,
        partial=partial
    )
    
    # Count results
    cards_count = len(results.get("cards", []))
    boards_count = len(results.get("boards", []))
    members_count = len(results.get("members", []))
    orgs_count = len(results.get("organizations", []))
    
    return f"Search results for '{query}': {cards_count} cards, {boards_count} boards, {members_count} members, {orgs_count} organizations. Full results: {json.dumps(results)}"



async def search_members(
    ctx: Context,
    query: str,
    limit: int = 8
) -> str:
    """
    Search for Trello members by name or email.
    
    Args:
        query: Search query string (name or email)
        limit: Maximum number of results (default 8, max 20)
        
    Returns:
        JSON string containing list of matching members
    """
    client = client
    # Using global service
    
    # Search members
    members = service.search_members(query, limit)
    
    return f"Found {len(members)} member(s) matching '{query}': {json.dumps(members)}"
