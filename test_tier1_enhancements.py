"""
Comprehensive test suite for Tier 1 enhancements.
Tests all new features: Members, Attachments, Comments, Labels, Webhooks.
"""

import os
import sys

# Set environment variables BEFORE any imports
os.environ["TRELLO_API_KEY"] = "test_key"
os.environ["TRELLO_TOKEN"] = "test_token"


def test_imports():
    """Test that all new modules can be imported."""
    print("Testing imports...")
    
    # DTOs
    from server.dtos.add_board_member import AddBoardMemberPayload
    from server.dtos.update_board_member import UpdateBoardMemberPayload
    from server.dtos.attach_url import AttachUrlPayload
    from server.dtos.add_comment import AddCommentPayload
    from server.dtos.update_comment import UpdateCommentPayload
    from server.dtos.update_label import UpdateLabelPayload
    from server.dtos.create_webhook import CreateWebhookPayload
    from server.dtos.update_webhook import UpdateWebhookPayload
    
    # Models
    from server.models import (
        TrelloMember, TrelloAttachment, TrelloAction,
        TrelloWebhook
    )
    
    # Services
    from server.services.member import MemberService
    from server.services.attachment import AttachmentService
    from server.services.comment import CommentService
    from server.services.label import LabelService
    from server.services.webhook import WebhookService
    
    # Tools
    from server.tools import member, attachment, comment, label, webhook
    
    print("✓ All imports successful")


def test_member_dtos():
    """Test member DTO validation."""
    print("\nTesting member DTOs...")
    
    from server.dtos.add_board_member import AddBoardMemberPayload
    from server.dtos.update_board_member import UpdateBoardMemberPayload
    from pydantic import ValidationError
    
    # Valid member payload
    payload = AddBoardMemberPayload(
        email="test@example.com",
        type="normal"
    )
    assert payload.email == "test@example.com"
    assert payload.type == "normal"
    
    # Invalid email
    try:
        AddBoardMemberPayload(email="invalid-email", type="normal")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass
    
    # Invalid type
    try:
        AddBoardMemberPayload(email="test@example.com", type="invalid")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass
    
    # Update member payload
    update_payload = UpdateBoardMemberPayload(type="admin")
    assert update_payload.type == "admin"
    
    print("✓ Member DTOs validated successfully")


def test_attachment_dtos():
    """Test attachment DTO validation."""
    print("\nTesting attachment DTOs...")
    
    from server.dtos.attach_url import AttachUrlPayload
    from pydantic import ValidationError
    
    # Valid URL payload
    payload = AttachUrlPayload(
        url="https://example.com/document.pdf",
        name="Important Document"
    )
    assert payload.url == "https://example.com/document.pdf"
    assert payload.name == "Important Document"
    
    # Invalid URL
    try:
        AttachUrlPayload(url="not-a-url")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass
    
    print("✓ Attachment DTOs validated successfully")


def test_comment_dtos():
    """Test comment DTO validation."""
    print("\nTesting comment DTOs...")
    
    from server.dtos.add_comment import AddCommentPayload
    from server.dtos.update_comment import UpdateCommentPayload
    from pydantic import ValidationError
    
    # Valid comment payload
    payload = AddCommentPayload(text="This is a test comment")
    assert payload.text == "This is a test comment"
    
    # Empty comment
    try:
        AddCommentPayload(text="")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass
    
    # Whitespace only
    try:
        AddCommentPayload(text="   ")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass
    
    # Update comment payload
    update_payload = UpdateCommentPayload(text="Updated comment")
    assert update_payload.text == "Updated comment"
    
    print("✓ Comment DTOs validated successfully")


def test_label_dtos():
    """Test label DTO validation."""
    print("\nTesting label DTOs...")
    
    from server.dtos.update_label import UpdateLabelPayload
    from pydantic import ValidationError
    
    # Valid label payload
    payload = UpdateLabelPayload(name="High Priority", color="red")
    assert payload.name == "High Priority"
    assert payload.color == "red"
    
    # Invalid color
    try:
        UpdateLabelPayload(color="invalid-color")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass
    
    # Valid null color
    payload = UpdateLabelPayload(color="null")
    assert payload.color == "null"
    
    print("✓ Label DTOs validated successfully")


def test_webhook_dtos():
    """Test webhook DTO validation."""
    print("\nTesting webhook DTOs...")
    
    from server.dtos.create_webhook import CreateWebhookPayload
    from server.dtos.update_webhook import UpdateWebhookPayload
    from pydantic import ValidationError
    
    # Valid webhook payload
    payload = CreateWebhookPayload(
        callback_url="https://example.com/webhook",
        id_model="5abbe4b7ddc1b351ef961414",
        description="Test webhook",
        active=True
    )
    assert payload.callback_url == "https://example.com/webhook"
    assert payload.id_model == "5abbe4b7ddc1b351ef961414"
    assert payload.active is True
    
    # Invalid callback URL
    try:
        CreateWebhookPayload(
            callback_url="not-a-url",
            id_model="5abbe4b7ddc1b351ef961414"
        )
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass
    
    # Update webhook payload
    update_payload = UpdateWebhookPayload(active=False)
    assert update_payload.active is False
    
    print("✓ Webhook DTOs validated successfully")


def test_models():
    """Test model instantiation."""
    print("\nTesting models...")
    
    from server.models import (
        TrelloMember, TrelloAttachment, TrelloAction, TrelloWebhook
    )
    
    # Member model
    member = TrelloMember(
        id="123",
        fullName="Test User",
        username="testuser",
        email="test@example.com"
    )
    assert member.id == "123"
    assert member.fullName == "Test User"
    
    # Attachment model
    attachment = TrelloAttachment(
        id="456",
        name="document.pdf",
        url="https://example.com/doc.pdf"
    )
    assert attachment.id == "456"
    assert attachment.name == "document.pdf"
    
    # Action model
    action = TrelloAction(
        id="789",
        type="commentCard",
        date="2024-01-01T00:00:00.000Z"
    )
    assert action.id == "789"
    assert action.type == "commentCard"
    
    # Webhook model
    webhook = TrelloWebhook(
        id="abc",
        idModel="def",
        callbackURL="https://example.com/webhook",
        active=True
    )
    assert webhook.id == "abc"
    assert webhook.active is True
    
    print("✓ All models instantiated successfully")


def test_service_methods():
    """Test that service methods exist."""
    print("\nTesting service methods...")
    
    from server.services.member import MemberService
    from server.services.attachment import AttachmentService
    from server.services.comment import CommentService
    from server.services.label import LabelService
    from server.services.webhook import WebhookService
    from server.utils.trello_api import TrelloClient
    
    client = TrelloClient(api_key="test_key", token="test_token")
    
    # Member service
    member_service = MemberService(client)
    assert hasattr(member_service, 'get_board_members')
    assert hasattr(member_service, 'add_board_member')
    assert hasattr(member_service, 'update_board_member')
    assert hasattr(member_service, 'remove_board_member')
    assert hasattr(member_service, 'get_workspace_members')
    assert hasattr(member_service, 'get_member')
    assert hasattr(member_service, 'get_card_members')
    assert hasattr(member_service, 'add_card_member')
    assert hasattr(member_service, 'remove_card_member')
    
    # Attachment service
    attachment_service = AttachmentService(client)
    assert hasattr(attachment_service, 'get_card_attachments')
    assert hasattr(attachment_service, 'attach_url')
    assert hasattr(attachment_service, 'delete_attachment')
    assert hasattr(attachment_service, 'set_attachment_as_cover')
    
    # Comment service
    comment_service = CommentService(client)
    assert hasattr(comment_service, 'get_card_comments')
    assert hasattr(comment_service, 'get_card_actions')
    assert hasattr(comment_service, 'add_comment')
    assert hasattr(comment_service, 'update_comment')
    assert hasattr(comment_service, 'delete_comment')
    assert hasattr(comment_service, 'get_board_actions')
    
    # Label service
    label_service = LabelService(client)
    assert hasattr(label_service, 'update_label')
    assert hasattr(label_service, 'delete_label')
    assert hasattr(label_service, 'get_card_labels')
    assert hasattr(label_service, 'add_label_to_card')
    assert hasattr(label_service, 'remove_label_from_card')
    
    # Webhook service
    webhook_service = WebhookService(client)
    assert hasattr(webhook_service, 'create_webhook')
    assert hasattr(webhook_service, 'get_webhook')
    assert hasattr(webhook_service, 'list_webhooks')
    assert hasattr(webhook_service, 'update_webhook')
    assert hasattr(webhook_service, 'delete_webhook')
    
    print("✓ All service methods exist")


def test_tool_functions():
    """Test that tool functions exist."""
    print("\nTesting tool functions...")
    
    from server.tools import member, attachment, comment, label, webhook
    
    # Member tools
    assert hasattr(member, 'get_board_members')
    assert hasattr(member, 'add_board_member')
    assert hasattr(member, 'update_board_member')
    assert hasattr(member, 'remove_board_member')
    assert hasattr(member, 'get_workspace_members')
    assert hasattr(member, 'get_member')
    assert hasattr(member, 'get_card_members')
    assert hasattr(member, 'add_card_member')
    assert hasattr(member, 'remove_card_member')
    
    # Attachment tools
    assert hasattr(attachment, 'get_card_attachments')
    assert hasattr(attachment, 'attach_url')
    assert hasattr(attachment, 'delete_attachment')
    assert hasattr(attachment, 'set_attachment_as_cover')
    
    # Comment tools
    assert hasattr(comment, 'get_card_comments')
    assert hasattr(comment, 'get_card_actions')
    assert hasattr(comment, 'add_comment')
    assert hasattr(comment, 'update_comment')
    assert hasattr(comment, 'delete_comment')
    assert hasattr(comment, 'get_board_actions')
    
    # Label tools
    assert hasattr(label, 'update_label')
    assert hasattr(label, 'delete_label')
    assert hasattr(label, 'get_card_labels')
    assert hasattr(label, 'add_label_to_card')
    assert hasattr(label, 'remove_label_from_card')
    
    # Webhook tools
    assert hasattr(webhook, 'create_webhook')
    assert hasattr(webhook, 'get_webhook')
    assert hasattr(webhook, 'list_webhooks')
    assert hasattr(webhook, 'update_webhook')
    assert hasattr(webhook, 'delete_webhook')
    
    print("✓ All tool functions exist")


def test_tools_registration():
    """Test that tools are properly registered."""
    print("\nTesting tools registration...")
    
    from server.tools.tools import register_tools
    
    # Mock MCP server
    class MockMCP:
        def __init__(self):
            self.tools = []
        
        def add_tool(self, tool):
            self.tools.append(tool)
    
    mcp = MockMCP()
    register_tools(mcp)
    
    # Should have all tools registered
    # Original: 6 board + 5 list + 5 card + 8 checklist + 6 workspace = 30
    # New: 9 member + 4 attachment + 6 comment + 5 label + 5 webhook = 29
    # Total: 59 tools
    assert len(mcp.tools) >= 55, f"Expected at least 55 tools, got {len(mcp.tools)}"
    
    print(f"✓ Tools registration successful ({len(mcp.tools)} tools registered)")


def main():
    """Run all tests."""
    print("=" * 60)
    print("TIER 1 ENHANCEMENTS TEST SUITE")
    print("=" * 60)
    
    try:
        test_imports()
        test_member_dtos()
        test_attachment_dtos()
        test_comment_dtos()
        test_label_dtos()
        test_webhook_dtos()
        test_models()
        test_service_methods()
        test_tool_functions()
        test_tools_registration()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nFeatures tested:")
        print("  • Member Management (9 operations)")
        print("  • Attachment Management (4 operations)")
        print("  • Comment Management (6 operations)")
        print("  • Enhanced Label Management (5 operations)")
        print("  • Webhook Support (5 operations)")
        print("\nTotal: 29 new operations added")
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
