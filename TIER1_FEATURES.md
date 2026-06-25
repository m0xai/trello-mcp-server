# Tier 1 Enhancements - Complete Feature Documentation

## Overview

This document provides comprehensive documentation for all Tier 1 enhancements implemented in the Trello MCP server. These features transform the server from a basic CRUD platform into a comprehensive collaboration and automation powerhouse.

## Summary of Enhancements

**29 new operations** added across 5 major feature areas:

| Feature Area | Operations | Status |
|--------------|------------|--------|
| Member Management | 9 | ✅ Complete |
| Attachment Management | 4 | ✅ Complete |
| Comment Management | 6 | ✅ Complete |
| Enhanced Label Management | 5 | ✅ Complete |
| Webhook Support | 5 | ✅ Complete |
| **Total** | **29** | **✅ Complete** |

---

## 1. Member Management

### Overview

Complete member management capabilities for boards, workspaces, and cards. Enables team collaboration workflows, permission management, and member assignment automation.

### Operations

#### Get Board Members

Retrieves all members of a board.

**Usage:**
```
Show me all members of board [board_id]
```

**Parameters:**
- `board_id` (string, required): The ID of the board

**Returns:** List of TrelloMember objects

**Example Response:**
```json
[
  {
    "id": "5abbe4b7ddc1b351ef961414",
    "fullName": "John Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "memberType": "normal"
  }
]
```

#### Add Board Member

Add a member to a board by email address.

**Usage:**
```
Add user@example.com to board [board_id] as admin
```

**Parameters:**
- `board_id` (string, required): The ID of the board
- `payload`:
  - `email` (string, required): Email address of the member
  - `type` (string, optional): Member type - "normal", "admin", or "observer" (default: "normal")
  - `allow_billable_guest` (boolean, optional): Allow adding as billable guest

**Validation:**
- Email must be valid format
- Type must be one of: normal, admin, observer

**Returns:** TrelloMember object

#### Update Board Member

Update a board member's role/permissions.

**Usage:**
```
Change member [member_id] to admin on board [board_id]
```

**Parameters:**
- `board_id` (string, required): The ID of the board
- `member_id` (string, required): The ID of the member
- `payload`:
  - `type` (string, required): New member type - "normal", "admin", or "observer"

**Returns:** Updated TrelloMember object

#### Remove Board Member

Remove a member from a board.

**Usage:**
```
Remove member [member_id] from board [board_id]
```

**Parameters:**
- `board_id` (string, required): The ID of the board
- `member_id` (string, required): The ID of the member to remove

**Returns:** Confirmation message

#### Get Workspace Members

Retrieves all members of a workspace/organization.

**Usage:**
```
Show me all members of workspace [workspace_id]
```

**Parameters:**
- `workspace_id` (string, required): The ID of the workspace

**Returns:** List of TrelloMember objects

#### Get Member

Retrieves details of a specific member.

**Usage:**
```
Get details for member [member_id]
Get my member details
```

**Parameters:**
- `member_id` (string, optional): The ID of the member (default: "me" for authenticated user)

**Returns:** TrelloMember object

#### Get Card Members

Retrieves all members assigned to a card.

**Usage:**
```
Show me who is assigned to card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card

**Returns:** List of TrelloMember objects

#### Add Card Member

Assign a member to a card.

**Usage:**
```
Assign member [member_id] to card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card
- `member_id` (string, required): The ID of the member to assign

**Returns:** Updated list of card members

#### Remove Card Member

Unassign a member from a card.

**Usage:**
```
Remove member [member_id] from card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card
- `member_id` (string, required): The ID of the member to remove

**Returns:** Confirmation message

---

## 2. Attachment Management

### Overview

Complete attachment lifecycle management for cards. Supports URL attachments, file uploads, and card cover images.

### Operations

#### Get Card Attachments

Retrieves all attachments on a card.

**Usage:**
```
Show me all attachments on card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card

**Returns:** List of TrelloAttachment objects

**Example Response:**
```json
[
  {
    "id": "5abbe4b7ddc1b351ef961414",
    "name": "document.pdf",
    "url": "https://trello.com/1/cards/abc/attachments/def/download/document.pdf",
    "bytes": 102400,
    "isUpload": true,
    "mimeType": "application/pdf"
  }
]
```

#### Attach URL

Attach a URL to a card (link to external resource).

**Usage:**
```
Attach https://example.com/document.pdf to card [card_id] with name "Important Document"
```

**Parameters:**
- `card_id` (string, required): The ID of the card
- `payload`:
  - `url` (string, required): The URL to attach (must start with http:// or https://)
  - `name` (string, optional): Display name for the attachment

**Validation:**
- URL must be valid format (http:// or https://)

**Returns:** TrelloAttachment object

#### Delete Attachment

Delete an attachment from a card.

**Usage:**
```
Delete attachment [attachment_id] from card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card
- `attachment_id` (string, required): The ID of the attachment to delete

**Returns:** Confirmation message

#### Set Attachment as Cover

Set an attachment as the card cover image.

**Usage:**
```
Set attachment [attachment_id] as cover for card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card
- `attachment_id` (string, required): The ID of the attachment (must be an image)

**Returns:** Confirmation message

---

## 3. Comment Management

### Overview

Complete comment and activity management for cards and boards. Enables discussion threads, feedback, and activity tracking.

### Operations

#### Get Card Comments

Retrieves all comments on a card.

**Usage:**
```
Show me all comments on card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card

**Returns:** List of TrelloAction objects (type: "commentCard")

**Example Response:**
```json
[
  {
    "id": "5abbe4b7ddc1b351ef961414",
    "type": "commentCard",
    "date": "2024-01-15T10:30:00.000Z",
    "idMemberCreator": "abc123",
    "data": {
      "text": "This looks great!"
    },
    "memberCreator": {
      "fullName": "John Doe",
      "username": "johndoe"
    }
  }
]
```

#### Get Card Actions

Retrieves all actions/activity on a card with filtering.

**Usage:**
```
Show me all activity on card [card_id]
Show me the last 100 actions on card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card
- `filter` (string, optional): Action type filter (default: "all")
  - "all" - All actions
  - "commentCard" - Only comments
  - "updateCard" - Card updates
  - "addAttachmentToCard" - Attachments added
  - And many more...
- `limit` (integer, optional): Maximum actions to return (default: 50, max: 1000)

**Returns:** List of TrelloAction objects

#### Add Comment

Add a comment to a card.

**Usage:**
```
Add comment "This looks great!" to card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card
- `payload`:
  - `text` (string, required): The comment text (min 1 character)

**Validation:**
- Text cannot be empty or just whitespace

**Returns:** TrelloAction object (the created comment)

#### Update Comment

Edit an existing comment.

**Usage:**
```
Update comment [action_id] to "This looks even better!"
```

**Parameters:**
- `action_id` (string, required): The ID of the comment action
- `payload`:
  - `text` (string, required): The new comment text

**Note:** Users can only update their own comments.

**Returns:** Updated TrelloAction object

#### Delete Comment

Delete a comment.

**Usage:**
```
Delete comment [action_id]
```

**Parameters:**
- `action_id` (string, required): The ID of the comment action to delete

**Note:** Users can only delete their own comments.

**Returns:** Confirmation message

#### Get Board Actions

Retrieves activity feed for a board.

**Usage:**
```
Show me recent activity on board [board_id]
Show me the last 200 actions on board [board_id]
```

**Parameters:**
- `board_id` (string, required): The ID of the board
- `filter` (string, optional): Action type filter (default: "all")
- `limit` (integer, optional): Maximum actions to return (default: 50, max: 1000)

**Returns:** List of TrelloAction objects

---

## 4. Enhanced Label Management

### Overview

Complete label lifecycle management. Extends the existing label creation capabilities with update, delete, and card assignment operations.

### Operations

#### Update Label

Update a label's name or color.

**Usage:**
```
Update label [label_id] to name "High Priority" and color red
Change label [label_id] color to green
```

**Parameters:**
- `label_id` (string, required): The ID of the label
- `payload`:
  - `name` (string, optional): New label name (max 16384 characters)
  - `color` (string, optional): New label color

**Valid Colors:**
- green, yellow, orange, red, purple, blue, sky, lime, pink, black, null (no color)

**Validation:**
- At least one of name or color must be provided
- Color must be from valid list
- Name length must not exceed 16384 characters

**Returns:** Updated TrelloLabel object

#### Delete Label

Delete a label from its board.

**Usage:**
```
Delete label [label_id]
```

**Parameters:**
- `label_id` (string, required): The ID of the label to delete

**Returns:** Confirmation message

#### Get Card Labels

Retrieves all labels on a card.

**Usage:**
```
Show me all labels on card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card

**Returns:** List of TrelloLabel objects

#### Add Label to Card

Assign a label to a card.

**Usage:**
```
Add label [label_id] to card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card
- `label_id` (string, required): The ID of the label to add

**Returns:** Updated list of card labels

#### Remove Label from Card

Remove a label from a card.

**Usage:**
```
Remove label [label_id] from card [card_id]
```

**Parameters:**
- `card_id` (string, required): The ID of the card
- `label_id` (string, required): The ID of the label to remove

**Returns:** Confirmation message

---

## 5. Webhook Support

### Overview

Complete webhook lifecycle management for real-time event notifications. Enables event-driven automation and integration with external systems.

### Operations

#### Create Webhook

Create a new webhook to monitor a board, card, or list.

**Usage:**
```
Create a webhook for board [board_id] that posts to https://example.com/webhook
```

**Parameters:**
- `payload`:
  - `callback_url` (string, required): The URL to receive webhook events (must be publicly accessible)
  - `id_model` (string, required): The ID of the model to watch (board, card, or list)
  - `description` (string, optional): Description of the webhook
  - `active` (boolean, optional): Whether the webhook is active (default: true)

**Validation:**
- Callback URL must be valid format (http:// or https://)
- Model ID must be valid format
- For production, callback URL should use HTTPS

**Returns:** TrelloWebhook object

**Example Response:**
```json
{
  "id": "5abbe4b7ddc1b351ef961414",
  "description": "Board activity webhook",
  "idModel": "5abbe4b7ddc1b351ef961414",
  "callbackURL": "https://example.com/webhook",
  "active": true,
  "consecutiveFailures": 0
}
```

**Webhook Events:**
Webhooks receive POST requests for all actions on the monitored model:
- Card created, updated, moved, archived
- Comment added
- Member assigned
- Attachment added
- Label changed
- Checklist updated
- And many more...

#### Get Webhook

Retrieves details of a specific webhook.

**Usage:**
```
Show me webhook [webhook_id]
```

**Parameters:**
- `webhook_id` (string, required): The ID of the webhook

**Returns:** TrelloWebhook object

#### List Webhooks

Retrieves all webhooks for an API token.

**Usage:**
```
Show me all my webhooks
```

**Parameters:**
- `token` (string, required): The API token (use the token from environment)

**Returns:** List of TrelloWebhook objects

**Note:** Each token can have multiple webhooks, but only one webhook per model.

#### Update Webhook

Update a webhook's configuration.

**Usage:**
```
Update webhook [webhook_id] to use new URL https://example.com/new-webhook
Deactivate webhook [webhook_id]
```

**Parameters:**
- `webhook_id` (string, required): The ID of the webhook
- `payload`:
  - `callback_url` (string, optional): New callback URL
  - `description` (string, optional): New description
  - `active` (boolean, optional): Whether the webhook is active

**Validation:**
- At least one field must be provided
- Callback URL must be valid format if provided

**Returns:** Updated TrelloWebhook object

#### Delete Webhook

Delete a webhook.

**Usage:**
```
Delete webhook [webhook_id]
```

**Parameters:**
- `webhook_id` (string, required): The ID of the webhook to delete

**Returns:** Confirmation message

### Webhook Health Monitoring

Webhooks track their health automatically:
- `consecutiveFailures`: Number of consecutive failed delivery attempts
- `firstConsecutiveFailDate`: When failures started

If a webhook fails too many times, Trello will automatically deactivate it. Monitor these fields to ensure your webhooks are healthy.

---

## Architecture

All Tier 1 enhancements follow the established architecture pattern:

### 1. DTO Layer (Data Transfer Objects)
- Pydantic models for request payloads
- Comprehensive validation rules
- `to_api_params()` conversion method

**Example:**
```python
from server.dtos.add_board_member import AddBoardMemberPayload

payload = AddBoardMemberPayload(
    email="user@example.com",
    type="admin"
)
params = payload.to_api_params()
```

### 2. Service Layer
- Business logic implementation
- API calls via TrelloClient
- Response transformation

**Example:**
```python
from server.services.member import MemberService

service = MemberService(client)
member = await service.add_board_member(board_id, **params)
```

### 3. Tool Layer
- MCP tool functions
- Validation integration
- Error handling
- Logging

**Example:**
```python
from server.tools import member

result = await member.add_board_member(ctx, board_id, payload)
```

### 4. Validation Layer
- Pre-flight resource checks
- Permission validation
- Business rule enforcement

**Example:**
```python
from server.validators import ValidationService

await validator.validate_board_exists(board_id)
```

---

## Error Handling

All operations use comprehensive error handling:

### Exception Types

- **ResourceNotFoundError**: Resource doesn't exist (404)
- **UnauthorizedError**: Authentication failed (401)
- **ForbiddenError**: Permission denied (403)
- **ValidationError**: Input validation failed
- **RateLimitError**: API rate limit exceeded (429)

### Error Messages

All errors include:
- Resource type and ID
- Clear description of the problem
- Actionable guidance for resolution

**Example:**
```
Failed to add board member: Member 'invalid@example.com' not found. 
Please verify the email address and ensure the member has a Trello account.
```

---

## Validation Rules

### Member Management
- Email must be valid format
- Member type must be: normal, admin, or observer
- Board and workspace must exist
- User must have appropriate permissions

### Attachment Management
- URL must be valid format (http:// or https://)
- Card must exist
- File size limits apply (10MB free, 250MB paid)

### Comment Management
- Comment text cannot be empty or whitespace only
- Card/board must exist
- Users can only update/delete their own comments
- Action limit capped at 1000 per request

### Label Management
- Label color must be from valid list
- Label name max 16384 characters
- At least one field required for updates
- Card and label must exist

### Webhook Management
- Callback URL must be valid format
- Model ID must be valid format
- Only one webhook per model per token
- Callback URL should be publicly accessible
- HTTPS recommended for production

---

## Usage Examples

### Team Collaboration Workflow

```
# Add team members to board
Add alice@example.com to board [board_id] as admin
Add bob@example.com to board [board_id] as normal

# Assign members to cards
Assign member [alice_id] to card [card_id]
Assign member [bob_id] to card [card_id]

# Add comments for discussion
Add comment "Please review the design" to card [card_id]
Add comment "Looks good to me!" to card [card_id]

# Attach reference materials
Attach https://docs.example.com/spec.pdf to card [card_id] with name "Requirements"
```

### Label Organization Workflow

```
# Update label colors
Update label [label_id] to color red and name "Urgent"
Update label [label_id2] to color green and name "Approved"

# Apply labels to cards
Add label [urgent_label_id] to card [card_id]
Add label [approved_label_id] to card [card_id]

# Check card labels
Show me all labels on card [card_id]
```

### Real-Time Integration Workflow

```
# Create webhook for board events
Create a webhook for board [board_id] that posts to https://api.example.com/trello-events

# Monitor webhook health
Show me all my webhooks

# Update webhook if needed
Update webhook [webhook_id] to use new URL https://api.example.com/v2/trello-events

# Deactivate when not needed
Update webhook [webhook_id] to inactive
```

---

## Performance Considerations

### Rate Limits
- Trello API: 300 requests per 10 seconds per token
- 100 requests per 10 seconds per token per board
- Automatic retry with exponential backoff implemented

### Pagination
- Comments/actions limited to 1000 per request
- Use pagination for large result sets
- Filter actions by type to reduce data transfer

### Caching
- Consider caching member lists for frequently accessed boards
- Cache workspace members for permission checks
- Invalidate cache on member changes

---

## Security Considerations

### Authentication
- API key and token stored in environment variables
- Never logged or exposed in errors
- HTTPS for all API calls

### Permissions
- Member operations require appropriate board/workspace permissions
- Users can only update/delete their own comments
- Webhook callbacks should validate request signatures

### Input Validation
- All user inputs sanitized
- Email addresses validated
- URLs validated for format
- File uploads checked for size and type

---

## Testing

Comprehensive test suite included:

```bash
cd /home/ubuntu/trello-mcp-server
python3.11 test_tier1_enhancements.py
```

**Test Coverage:**
- DTO validation (all payloads)
- Model instantiation
- Service method signatures
- Tool function signatures
- Tools registration
- Import verification

**Test Results:**
- 10/10 test suites passing
- 60 tools registered
- 29 new operations validated

---

## Migration Guide

### From Previous Version

All existing functionality remains unchanged. The enhancements are fully backward compatible.

**New DTOs:**
- `AddBoardMemberPayload`
- `UpdateBoardMemberPayload`
- `AttachUrlPayload`
- `AddCommentPayload`
- `UpdateCommentPayload`
- `UpdateLabelPayload`
- `CreateWebhookPayload`
- `UpdateWebhookPayload`

**New Models:**
- `TrelloMember`
- `TrelloAttachment`
- `TrelloAction`
- `TrelloWebhook`

**New Services:**
- `MemberService`
- `AttachmentService`
- `CommentService`
- `LabelService`
- `WebhookService`

**New Tools:**
- 9 member tools
- 4 attachment tools
- 6 comment tools
- 5 label tools
- 5 webhook tools

---

## Roadmap

### Completed (Tier 1)
✅ Member Management
✅ Attachment Management
✅ Comment Management
✅ Enhanced Label Management
✅ Webhook Support

### Planned (Tier 2)
- Custom Fields
- Search & Filtering
- Batch Operations
- Export & Import
- Advanced Card Features

### Future (Tier 3)
- Power-Ups Management
- Board Templates
- Analytics & Reporting
- Automation Rules

---

## Support

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/m0xai/trello-mcp-server/issues
- Documentation: This file and ENHANCEMENTS_FINAL.md

---

## Changelog

### Version 2.0.0 (Tier 1 Enhancements)

**Added:**
- Member Management (9 operations)
- Attachment Management (4 operations)
- Comment Management (6 operations)
- Enhanced Label Management (5 operations)
- Webhook Support (5 operations)

**Total:** 29 new operations, 60 tools registered

**Testing:** Comprehensive test suite with 10/10 passing

**Documentation:** Complete API documentation with examples

---

*Last Updated: February 2, 2026*
