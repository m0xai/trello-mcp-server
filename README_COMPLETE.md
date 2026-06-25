# Trello MCP Server - Complete CRUD Edition

A powerful MCP server for interacting with Trello boards, lists, cards, and workspaces via AI Hosts. **Now with complete CRUD operations for all major resources including workspaces!**

## 🎉 What's New in Version 2.1

### **Complete Workspace CRUD Operations**
- ✅ **Create workspaces** - Build new workspaces programmatically
- ✅ **Read workspaces** - List and view workspace details
- ✅ **Update workspaces** - Modify workspace settings
- ✅ **Delete workspaces** - Remove workspaces with permission validation

### Enhanced Board Operations
- ✅ **Create boards** with customizable settings
- ✅ **Update boards** - change name, description, visibility, and more
- ✅ **Delete boards** with permission validation
- ✅ **Move boards** between workspaces

### Comprehensive Validation
- ✅ **Resource existence checks** before operations
- ✅ **Permission validation** for destructive actions
- ✅ **Input validation** with clear error messages
- ✅ **Business rule enforcement** (name lengths, valid values, etc.)

### Enhanced Error Handling
- ✅ **Specific exception types** for different errors
- ✅ **Automatic retry logic** with exponential backoff
- ✅ **Rate limit handling** with Retry-After support
- ✅ **Clear, actionable error messages**

## Table of Contents

*   [Prerequisites](#prerequisites)
*   [Pre-installation](#pre-installation)
*   [Installation](#installation)
*   [Server Modes](#server-modes)
*   [Configuration](#configuration)
*   [Client Integration](#client-integration)
*   [Capabilities](#capabilities)
*   [New Features](#new-features)
*   [Usage](#usage)
*   [Troubleshooting](#troubleshooting)
*   [Contributing](#contributing)

## Prerequisites

1.  Python 3.12 or higher, can easily be managed by `uv`
2.  [Claude for Desktop](https://claude.ai/download) installed
3.  Trello account and API credentials
4.  [uv](https://docs.astral.sh/uv/) package manager installed

## Pre-installation

1.  Make sure you have installed Claude Desktop App
2.  Make sure you have already logged in with your account into Claude.
3.  Start Claude

## Installation

1.  Set up Trello API credentials:
    
    *   Go to [Trello Apps Administration](https://trello.com/power-ups/admin)
    *   Create a new integration at [New Power-Up or Integration](https://trello.com/power-ups/admin)
    *   Fill in your information (you can leave the Iframe connector URL empty) and make sure to select the correct Workspace
    *   Click your app's icon and navigate to "API key" from left sidebar.
    *   Copy your "API key" and on the right side: "you can manually generate a Token." click the word token to get your Trello Token.
2.  Rename the `.env.example` file in the project root with `.env` and set variables you just got:
    

```shell
TRELLO_API_KEY=your_api_key_here
TRELLO_TOKEN=your_token_here
```

3.  Install uv if you haven't already:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

4.  Clone this repository:

```shell
git clone https://github.com/m0xai/trello-mcp-server.git
cd trello-mcp-server
```

5.  Install dependencies and set server for Claude using uv:

```shell
uv run mcp install main.py
```

6.  Restart Claude Desktop app

## Server Modes

This MCP server can run in two different modes:

### Claude App Mode

This mode integrates directly with the Claude Desktop application:

1.  Set `USE_CLAUDE_APP=true` in your `.env` file (this is the default)
2.  Run the server with:

```shell
uv run mcp install main.py
```

3.  Restart the Claude Desktop application

### SSE Server Mode

This mode runs as a standalone SSE server that can be used with any MCP-compatible client, including Cursor:

1.  Set `USE_CLAUDE_APP=false` in your `.env` file
2.  Run the server with:

```shell
python main.py
```

3.  The server will be available at `http://localhost:8000` by default (or your configured port)

### Docker Mode

You can also run the server using Docker Compose:

1.  Make sure you have Docker and Docker Compose installed
2.  Create your `.env` file with your configuration
3.  Build and start the container:

```shell
docker-compose up -d
```

4.  The server will run in SSE mode by default
5.  To view logs:

```shell
docker-compose logs -f
```

6.  To stop the server:

```shell
docker-compose down
```

## Configuration

The server can be configured using environment variables in the `.env` file:

| Variable | Description | Default |
| --- | --- | --- |
| TRELLO\_API\_KEY | Your Trello API key | Required |
| TRELLO\_TOKEN | Your Trello API token | Required |
| MCP\_SERVER\_NAME | The name of the MCP server | Trello MCP Server |
| MCP\_SERVER\_HOST | Host address for SSE mode | 0.0.0.0 |
| MCP\_SERVER\_PORT | Port for SSE mode | 8000 |
| USE\_CLAUDE\_APP | Whether to use Claude app mode | true |

You can customize the server by editing these values in your `.env` file.

## Client Integration

### Using with Claude Desktop

1.  Run the server in Claude app mode (`USE_CLAUDE_APP=true`)
2.  Start or restart Claude Desktop
3.  Claude will automatically detect and connect to your MCP server

### Using with Cursor

To connect your MCP server to Cursor:

1.  Run the server in SSE mode (`USE_CLAUDE_APP=false`)
2.  In Cursor, go to Settings (gear icon) > AI > Model Context Protocol
3.  Add a new server with URL `http://localhost:8000` (or your configured host/port)
4.  Select the server when using Cursor's AI features

You can also add this configuration to your Cursor settings JSON file (typically at `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "trello": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

## Capabilities - Complete CRUD

| Operation | Board | List | Card | Checklist | Checklist Item | Workspace |
|-----------|-------|------|------|-----------|----------------|-----------|
| Read      | ✅    | ✅   | ✅   | ✅        | ✅             | ✅        |
| Write     | ✅    | ✅   | ✅   | ✅        | ✅             | **✅**    |
| Update    | ✅    | ✅   | ✅   | ✅        | ✅             | ✅        |
| Delete    | ✅    | ✅   | ✅   | ✅        | ✅             | **✅**    |

**All major resources now support complete CRUD operations!**

### Detailed Capabilities

#### Board Operations

*   ✅ Read all boards
*   ✅ Read specific board details
*   ✅ Create new boards
*   ✅ Update board settings
*   ✅ Delete boards
*   ✅ Get board labels
*   ✅ Create board labels

#### List Operations

*   ✅ Read all lists in a board
*   ✅ Read specific list details
*   ✅ Create new lists
*   ✅ Update list name
*   ✅ Archive (delete) lists

#### Card Operations

*   ✅ Read all cards in a list
*   ✅ Read specific card details
*   ✅ Create new cards
*   ✅ Update card attributes
*   ✅ Delete cards

#### Checklist Operations

*   ✅ Get a specific checklist
*   ✅ List all checklists in a card
*   ✅ Create a new checklist
*   ✅ Update a checklist
*   ✅ Delete a checklist
*   ✅ Add checkitem to checklist
*   ✅ Update checkitem
*   ✅ Delete checkitem

#### Workspace Operations - **COMPLETE CRUD**

*   ✅ **List all workspaces**
*   ✅ **Get workspace details**
*   ✅ **List boards in workspace**
*   ✅ **Create new workspaces** *(NEW)*
*   ✅ **Update workspace settings**
*   ✅ **Delete workspaces** *(NEW)*

## New Features

### Board Management

**Create a Board**
```
Create a new board called "Project Alpha" in my workspace
```

**Update a Board**
```
Update board [board_id] to make it public and enable voting
```

**Delete a Board**
```
Delete board [board_id]
```

**Move Board to Workspace**
```
Move board [board_id] to workspace [workspace_id]
```

### **Workspace Management - Complete CRUD**

**Create Workspace** *(NEW)*
```
Create a new workspace called "Engineering Team" with description "Our engineering workspace"
```

**List Workspaces**
```
Show me all my workspaces
```

**Get Workspace Details**
```
Get details for workspace [workspace_id]
```

**List Workspace Boards**
```
List all boards in workspace [workspace_id]
```

**Update Workspace**
```
Update workspace [workspace_id] to change the name to "Engineering Team"
```

**Delete Workspace** *(NEW)*
```
Delete workspace [workspace_id]
```

### Enhanced Validation

All operations now include:
- Resource existence verification
- Permission checks for destructive operations
- Input format validation
- Clear error messages with actionable guidance

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

## Usage

Once installed, you can interact with your Trello boards and workspaces through Claude. Here are some example queries:

### Basic Operations
*   "Show me all my boards"
*   "What lists are in board \[board\_name\]?"
*   "Create a new card in list \[list\_name\] with title \[title\]"
*   "Update the description of card \[card\_name\]"
*   "Archive the list \[list\_name\]"

### Board Operations
*   "Create a new board called 'Q1 Planning' in my workspace"
*   "Update board \[board_id\] to make it public"
*   "Change the name of board \[board_id\] to 'New Name'"
*   "Delete board \[board_id\]"
*   "Move board \[board_id\] to workspace \[workspace_id\]"

### **Workspace Operations - Complete CRUD**
*   "Create a new workspace called 'Product Team'"
*   "Show me all my workspaces"
*   "List all boards in workspace \[workspace_id\]"
*   "Get details for workspace \[workspace_id\]"
*   "Update workspace \[workspace_id\] description to 'Our product development workspace'"
*   "Delete workspace \[workspace_id\]"

## Troubleshooting

If you encounter issues:

1.  **Verify your Trello API credentials** in the `.env` file
2.  **Check permissions** - Ensure you have proper permissions in your Trello workspace
3.  **Update Claude** - Ensure Claude for Desktop is running the latest version
4.  **Check logs** - View error messages with `uv run mcp dev main.py` command
5.  **Verify uv installation** - Make sure uv is properly installed and in your PATH

### Common Issues

**"Workspace not found" errors**
- Verify the workspace ID is correct (24-character hexadecimal)
- Ensure you have access to the workspace
- Check if the workspace has been deleted

**"Board not found" errors**
- Verify the board ID is correct (24-character hexadecimal)
- Ensure you have access to the board
- Check if the board has been deleted

**"Permission denied" errors**
- Verify you're a board/workspace admin for destructive operations
- Check workspace membership for organization boards
- Ensure API token has proper scopes

**"Rate limit exceeded" errors**
- Wait for the specified retry period
- The server will automatically retry with exponential backoff
- Reduce frequency of API calls if this persists

**Validation errors**
- Check input formats match requirements
- Verify required fields are provided
- Review field length constraints in error messages
- Ensure workspace names use lowercase only

## Contributing

Feel free to submit issues and enhancement requests!

## Documentation

For detailed information about the enhancements, see:
- [ENHANCEMENTS_FINAL.md](ENHANCEMENTS_FINAL.md) - Complete documentation of all features including workspace CRUD
- [Design Document](trello_mcp_enhancement_design.md) - Technical design and architecture

## About

A comprehensive MCP server for Trello with complete CRUD operations for all major resources.

## License

Same as the original Trello MCP Server project.

## Changelog

### Version 2.1 (Complete CRUD)

**Added**
- **Workspace creation** - Create new workspaces with full validation
- **Workspace deletion** - Delete workspaces with permission checks
- CreateWorkspacePayload DTO with comprehensive validation
- Complete CRUD operations for workspaces

**Enhanced**
- WorkspaceService with create and delete methods
- Workspace tools with complete CRUD capabilities
- Documentation updated with workspace CRUD examples

### Version 2.0 (Enhanced)

**Added**
- Full CRUD operations for boards (create, update, delete)
- Workspace/organization management tools (read, update)
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

### Version 1.0 (Original)

- Basic board, list, card, and checklist operations
- Read operations for all resources
- Write operations for lists, cards, and checklists
- Claude Desktop and SSE server modes
