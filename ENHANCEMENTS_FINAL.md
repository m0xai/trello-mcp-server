# Trello MCP Server Enhancements - Complete Edition

## Overview

This document describes the comprehensive enhancements made to the Trello MCP Server, including new features, improved validation, and enhanced error handling. **Now with full CRUD operations for both boards and workspaces.**

## What's New

### Enhanced Board Operations

The server now supports full CRUD operations for boards:

**Create Board** - Create new Trello boards with customizable settings
- Set board name and description
- Choose visibility (private, org, public)
- Add to organization/workspace
- Configure default lists and labels
- Set voting and commenting permissions

**Update Board** - Modify existing boards
- Change board name and description
- Update visibility settings
- Move boards between workspaces
- Archive/unarchive boards
- Adjust board preferences

**Delete Board** - Permanently remove boards
- Validates admin permissions before deletion
- Provides clear confirmation messages

### **NEW: Complete Workspace Operations**

Full workspace/organization CRUD capabilities:

**Create Workspace** - Create new workspaces/organizations
- Set display name (required)
- Add description
- Choose short name for URL
- Set website URL
- Full validation of all inputs

**Read Workspaces** - View workspace information
- List all workspaces you're a member of
- Get detailed workspace information
- List all boards in a workspace with filtering

**Update Workspace** - Modify workspace settings
- Change display name and description
- Update workspace URL name
- Set website URL

**Delete Workspace** - Permanently remove workspaces
- Validates workspace exists before deletion
- Requires admin permissions
- Provides clear confirmation messages

### Comprehensive Validation

All operations now include pre-flight validation:

**Resource Existence Checks** - Verify resources exist before operations
- Boards, lists, cards, checklists, and workspaces
- Clear error messages when resources not found

**Permission Validation** - Ensure proper access rights
- Admin permission checks for destructive operations
- Workspace membership verification
- Access permission validation

**Input Validation** - Validate all inputs before API calls
- Field format validation (URLs, IDs, names)
- Required field checks
- Value range and constraint validation
- Pydantic models with custom validators

**Business Rule Validation** - Enforce Trello's business rules
- Board name length limits (1-16384 characters)
- Workspace name format (lowercase alphanumeric, min 3 chars)
- Valid permission levels and filter values
- Color validation for labels
- URL format validation

### Enhanced Error Handling

**Specific Exception Types** - Clear, actionable error messages
- `ResourceNotFoundError` - Resource doesn't exist (404)
- `UnauthorizedError` - Authentication failed (401)
- `ForbiddenError` - Permission denied (403)
- `RateLimitError` - API rate limit exceeded (429)
- `ValidationError` - Input validation failed (400)
- `BadRequestError` - Malformed request (400)

**Automatic Retry Logic** - Resilient API calls
- Exponential backoff for rate limits
- Configurable retry attempts (default: 3)
- Network error recovery
- Respects Retry-After headers

**Improved Error Messages** - User-friendly feedback
- Specific resource types and IDs in messages
- Actionable suggestions for resolution
- Clear indication of what went wrong

## **Updated Capabilities Table - COMPLETE CRUD**

| Operation | Board | List | Card | Checklist | Checklist Item | Workspace |
|-----------|-------|------|------|-----------|----------------|-----------|
| Read      | ✅    | ✅   | ✅   | ✅        | ✅             | ✅        |
| Write     | ✅    | ✅   | ✅   | ✅        | ✅             | **✅**    |
| Update    | ✅    | ✅   | ✅   | ✅        | ✅             | ✅        |
| Delete    | ✅    | ✅   | ✅   | ✅        | ✅             | **✅**    |

**All major resources now have complete CRUD operations!**

## New Tools

### Board Tools

**`create_board`**
```python
create_board(
    name: str,
    desc: Optional[str] = None,
    id_organization: Optional[str] = None,
    default_lists: bool = True,
    default_labels: bool = True,
    prefs_permission_level: str = "private",
    prefs_voting: Optional[str] = None,
    prefs_comments: Optional[str] = None
) -> TrelloBoard
```

**`update_board`**
```python
update_board(
    board_id: str,
    name: Optional[str] = None,
    desc: Optional[str] = None,
    closed: Optional[bool] = None,
    id_organization: Optional[str] = None,
    prefs_permission_level: Optional[str] = None,
    prefs_voting: Optional[str] = None,
    prefs_comments: Optional[str] = None,
    prefs_self_join: Optional[bool] = None,
    prefs_card_covers: Optional[bool] = None
) -> TrelloBoard
```

**`delete_board`**
```python
delete_board(board_id: str) -> dict
```

### Workspace Tools

**`get_workspaces`**
```python
get_workspaces() -> List[TrelloOrganization]
```

**`get_workspace`**
```python
get_workspace(workspace_id: str) -> TrelloOrganization
```

**`get_workspace_boards`**
```python
get_workspace_boards(
    workspace_id: str,
    filter_value: str = "all"  # all, open, closed, members, organization, public
) -> List[TrelloBoard]
```

**`create_workspace`** *(NEW)*
```python
create_workspace(
    display_name: str,  # REQUIRED
    desc: Optional[str] = None,
    name: Optional[str] = None,  # Short name for URL (lowercase, alphanumeric, underscores)
    website: Optional[str] = None
) -> TrelloOrganization
```

**`update_workspace`**
```python
update_workspace(
    workspace_id: str,
    display_name: Optional[str] = None,
    desc: Optional[str] = None,
    name: Optional[str] = None,
    website: Optional[str] = None
) -> TrelloOrganization
```

**`delete_workspace`** *(NEW)*
```python
delete_workspace(workspace_id: str) -> dict
```

## Usage Examples

### Creating a Board

```
Create a new board called "Project Alpha" in my workspace
```

The AI will:
1. Validate the workspace exists
2. Verify you're a member
3. Create the board with default settings
4. Return the new board details

### Updating a Board

```
Update board [board_id] to make it public and enable voting
```

The AI will:
1. Verify the board exists
2. Validate the permission level
3. Update the board settings
4. Return the updated board

### **Creating a Workspace (NEW)**

```
Create a new workspace called "Engineering Team" with description "Our engineering workspace"
```

The AI will:
1. Validate the display name is provided
2. Validate the short name format (if provided)
3. Create the workspace
4. Return the new workspace details

### **Deleting a Workspace (NEW)**

```
Delete workspace [workspace_id]
```

The AI will:
1. Verify the workspace exists
2. Check admin permissions (API enforces this)
3. Permanently delete the workspace
4. Return confirmation message

### Managing Workspaces

```
Show me all my workspaces
```

```
List all boards in workspace [workspace_id]
```

```
Update workspace [workspace_id] to change the name to "Engineering Team"
```

### Error Handling Examples

**Resource Not Found**
```
Error: Board '507f1f77bcf86cd799439011' not found. Please verify the ID and try again.
```

**Permission Denied**
```
Error: Permission denied to modify Board '507f1f77bcf86cd799439011'. Check your board/workspace permissions.
```

**Validation Error**
```
Error: Invalid permission level 'invalid'. Must be one of: private, org, public
```

**Workspace Creation Error**
```
Error: Workspace name must be at least 3 characters and contain only lowercase letters, numbers, and underscores
```

**Rate Limit**
```
Error: Trello API rate limit exceeded. Please retry after 60 seconds.
```

## Architecture Changes

### New Modules

**`server/exceptions.py`** - Custom exception hierarchy for clear error handling

**`server/validators/`** - Validation service for resource and permission checks
- `validation_service.py` - Core validation logic

**`server/dtos/`** - Data Transfer Objects with Pydantic validation
- `create_board.py` - Board creation payload
- `update_board.py` - Board update payload
- `create_workspace.py` - **NEW: Workspace creation payload**
- `update_workspace.py` - Workspace update payload

**`server/services/workspace.py`** - Workspace/organization service layer with full CRUD

**`server/tools/workspace.py`** - Workspace MCP tools with full CRUD

### Enhanced Modules

**`server/utils/trello_api.py`** - Enhanced with:
- Specific error handling by HTTP status code
- Automatic retry logic with exponential backoff
- Rate limit handling
- Improved logging

**`server/models.py`** - Added:
- `TrelloOrganization` model for workspaces

**`server/services/board.py`** - Added:
- `create_board()` method
- `update_board()` method
- `delete_board()` method

**`server/services/workspace.py`** - **Enhanced with:**
- `create_workspace()` method *(NEW)*
- `delete_workspace()` method *(NEW)*

**`server/tools/board.py`** - Added:
- Validation for all operations
- New tool functions for create, update, delete
- Enhanced error handling

**`server/tools/workspace.py`** - **Enhanced with:**
- `create_workspace` tool *(NEW)*
- `delete_workspace` tool *(NEW)*
- Validation for all operations

**`server/tools/list.py`** - Enhanced with:
- Pre-flight validation for all operations
- Improved error messages

**`server/tools/tools.py`** - **Updated with:**
- Registration of `create_workspace` *(NEW)*
- Registration of `delete_workspace` *(NEW)*

## Validation Rules

### Board Operations

**Board Name**
- Required for creation
- Length: 1-16384 characters
- Cannot be empty or whitespace only

**Permission Levels**
- Must be one of: `private`, `org`, `public`

**Voting/Comments Permissions**
- Must be one of: `disabled`, `members`, `observers`, `org`, `public`

**Organization ID**
- Must be valid 24-character hexadecimal string
- Organization must exist
- User must be a member

### **Workspace Operations (Enhanced)**

**Display Name**
- **Required** for creation
- Length: 1-16384 characters
- Cannot be empty or whitespace only

**Workspace Name (Short Name)**
- Optional, but if provided:
- Minimum 3 characters
- Lowercase alphanumeric and underscores only
- Pattern: `^[a-z0-9_]{3,}$`
- Used in workspace URL

**Website URL**
- Optional, but if provided:
- Must be valid HTTP or HTTPS URL
- Proper domain format required

**Description**
- Optional
- Maximum 16384 characters

### General Validation

**Resource IDs**
- Must be 24-character hexadecimal strings
- Format: `^[a-f0-9]{24}$`

**Filter Values**
- Board filters: `all`, `open`, `closed`, `members`, `organization`, `public`

## Migration Guide

### For Existing Users

All existing functionality remains unchanged. New features are additive and backward compatible.

**No Breaking Changes**
- Existing tool signatures unchanged
- Error handling enhanced but compatible
- New tools don't affect existing workflows

**New Capabilities**
- Can now create workspaces programmatically
- Can delete workspaces with proper permissions
- Full automation of workspace lifecycle

**Gradual Adoption**
- Use new features as needed
- Existing integrations continue to work
- Enhanced error messages provide better feedback

### For Developers

**Import Changes**
```python
# New imports available
from server.exceptions import TrelloMCPError, ValidationError
from server.validators import ValidationService
from server.dtos.create_board import CreateBoardPayload
from server.dtos.create_workspace import CreateWorkspacePayload  # NEW
```

**Using Validation Service**
```python
from server.validators import ValidationService
from server.trello import client

validator = ValidationService(client)

# Validate before operations
await validator.validate_board_exists(board_id)
await validator.validate_organization_exists(workspace_id)
await validator.validate_organization_membership(workspace_id)
```

**Error Handling**
```python
from server.exceptions import TrelloMCPError, ResourceNotFoundError

try:
    result = await service.get_board(board_id)
except ResourceNotFoundError as e:
    logger.error(f"Board not found: {e.message}")
except TrelloMCPError as e:
    logger.error(f"Operation failed: {e.message}")
```

## Performance Considerations

**Validation Overhead**
- Minimal: Validation checks use lightweight API calls
- Optimized: Only necessary fields requested (e.g., `fields=id`)
- Cached: Consider implementing caching for frequently accessed resources

**Retry Logic**
- Default: 3 retry attempts with exponential backoff
- Configurable: Adjust `max_retries` in TrelloClient initialization
- Smart: Only retries on rate limits and network errors

**API Call Efficiency**
- Validation checks combined where possible
- Batch operations not affected
- Rate limit handling prevents wasted calls

## Security Enhancements

**Input Sanitization**
- All inputs validated through Pydantic models
- SQL injection not applicable (REST API)
- XSS prevention through proper encoding

**Permission Verification**
- Admin checks before destructive operations
- Workspace membership validation
- Access rights verified before modifications

**Credential Protection**
- API keys and tokens remain in environment variables
- Never logged or exposed in error messages
- Secure transmission via HTTPS

## Testing

### Validation Testing

Test validation logic with various inputs:
- Valid and invalid resource IDs
- Empty and oversized strings
- Invalid permission levels
- Malformed URLs
- Invalid workspace names

### Integration Testing

Test full operation flows:
- Create board with/without organization
- Create workspace with various configurations
- Update board with various field combinations
- Delete board with proper/improper permissions
- Delete workspace with proper/improper permissions
- Workspace operations with filters

### Error Scenario Testing

Test error handling:
- Non-existent resources (404)
- Permission denied (403)
- Invalid inputs (400)
- Rate limiting (429)

## Troubleshooting

### Common Issues

**"Workspace not found" errors**
- Verify workspace ID is correct (24-character hex)
- Ensure you have access to the workspace
- Check if workspace has been deleted

**"Board not found" errors**
- Verify board ID is correct (24-character hex)
- Ensure you have access to the board
- Check if board has been deleted

**"Permission denied" errors**
- Verify you're a board/workspace admin for destructive operations
- Check workspace membership for organization boards
- Ensure API token has proper scopes

**"Rate limit exceeded" errors**
- Wait for the specified retry period
- Reduce frequency of API calls
- Implement caching for read operations

**Validation errors**
- Check input formats match requirements
- Verify required fields are provided
- Review field length constraints
- Ensure workspace names use lowercase only

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show:
- Validation checks performed
- API calls made
- Retry attempts
- Detailed error information

## Future Enhancements

Potential future improvements:
- Board templates support
- Bulk operations (create multiple boards/workspaces)
- Advanced filtering and search
- Webhook management
- Custom field operations
- Power-Up management
- Member management tools
- Board copying and cloning
- Workspace member management

## Support

For issues or questions:
1. Check error messages for specific guidance
2. Review validation rules in this document
3. Enable debug logging for detailed information
4. Submit issues on GitHub repository

## Changelog

### Version 2.1 (Current - Complete CRUD)

**Added**
- **Workspace creation** - Create new workspaces with full validation
- **Workspace deletion** - Delete workspaces with permission checks
- CreateWorkspacePayload DTO with comprehensive validation
- Full CRUD operations for workspaces

**Enhanced**
- WorkspaceService with create and delete methods
- Workspace tools with complete CRUD capabilities
- Documentation updated with workspace CRUD examples

### Version 2.0 (Enhanced)

**Added**
- Full CRUD operations for boards
- Workspace/organization management (read/update)
- Comprehensive validation framework
- Enhanced error handling with specific exceptions
- Automatic retry logic for rate limits
- Pre-flight validation for all operations
- Pydantic DTOs for type safety

**Enhanced**
- Error messages now more specific and actionable
- All operations include resource existence checks
- Improved logging throughout
- Better permission validation

**Fixed**
- Inconsistent error handling across tools
- Missing validation for destructive operations
- Unclear error messages

## License

Same as the original Trello MCP Server project.
