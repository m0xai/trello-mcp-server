"""
MCP tools for batch operations.
"""

import json
from mcp.server.fastmcp import Context
from server.trello import client
from server.validators import ValidationService

service = BatchService(client)
validator = ValidationService(client)
from server.services.batch import BatchService



async def batch_get_resources(
    urls: str,
    ctx: Context
) -> str:
    """
    Execute multiple GET requests in a single batch operation.
    
    This reduces API calls and improves performance when fetching multiple resources.
    Maximum 10 URLs per batch.
    
    Args:
        urls: Comma-separated list of relative URLs (e.g., "/boards/abc123,/cards/def456")
        
    Returns:
        JSON string containing array of responses
    """
    client = client
    # Using global service
    
    # Split URLs
    url_list = [url.strip() for url in urls.split(",")]
    
    if len(url_list) > 10:
        return f"Error: Maximum 10 URLs allowed per batch request. You provided {len(url_list)}."
    
    # Execute batch
    results = service.batch_get(url_list)
    
    return f"Batch request completed for {len(url_list)} URLs. Results: {json.dumps(results)}"
