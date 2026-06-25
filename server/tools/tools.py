"""
This module contains tools for managing Trello boards, lists, cards, and workspaces.
"""

from server.tools import (
    advanced_card,
    analytics,
    attachment,
    batch,
    board,
    card,
    checklist,
    comment,
    custom_field,
    export,
    label,
    list,
    member,
    search,
    webhook,
    workspace
)


def register_tools(mcp):
    """Register tools with the MCP server."""
    # Board Tools
    mcp.add_tool(board.get_board)
    mcp.add_tool(board.get_boards)
    mcp.add_tool(board.get_board_labels)
    mcp.add_tool(board.create_board_label)
    mcp.add_tool(board.create_board)
    mcp.add_tool(board.update_board)
    mcp.add_tool(board.delete_board)

    # List Tools
    mcp.add_tool(list.get_list)
    mcp.add_tool(list.get_lists)
    mcp.add_tool(list.create_list)
    mcp.add_tool(list.update_list)
    mcp.add_tool(list.delete_list)

    # Card Tools
    mcp.add_tool(card.get_card)
    mcp.add_tool(card.get_cards)
    mcp.add_tool(card.create_card)
    mcp.add_tool(card.update_card)
    mcp.add_tool(card.delete_card)

    # Checklist Tools
    mcp.add_tool(checklist.get_checklist)
    mcp.add_tool(checklist.get_card_checklists)
    mcp.add_tool(checklist.create_checklist)
    mcp.add_tool(checklist.update_checklist)
    mcp.add_tool(checklist.delete_checklist)
    mcp.add_tool(checklist.add_checkitem)
    mcp.add_tool(checklist.update_checkitem)
    mcp.add_tool(checklist.delete_checkitem)

    # Label Tools
    mcp.add_tool(label.update_label)
    mcp.add_tool(label.delete_label)
    mcp.add_tool(label.get_card_labels)
    mcp.add_tool(label.add_label_to_card)
    mcp.add_tool(label.remove_label_from_card)

    # Comment Tools
    mcp.add_tool(comment.get_card_comments)
    mcp.add_tool(comment.get_card_actions)
    mcp.add_tool(comment.add_comment)
    mcp.add_tool(comment.update_comment)
    mcp.add_tool(comment.delete_comment)
    mcp.add_tool(comment.get_board_actions)

    # Attachment Tools
    mcp.add_tool(attachment.get_card_attachments)
    mcp.add_tool(attachment.attach_url)
    mcp.add_tool(attachment.delete_attachment)
    mcp.add_tool(attachment.set_attachment_as_cover)

    # Member Tools
    mcp.add_tool(member.get_board_members)
    mcp.add_tool(member.add_board_member)
    mcp.add_tool(member.update_board_member)
    mcp.add_tool(member.remove_board_member)
    mcp.add_tool(member.get_workspace_members)
    mcp.add_tool(member.get_member)
    mcp.add_tool(member.get_card_members)
    mcp.add_tool(member.add_card_member)
    mcp.add_tool(member.remove_card_member)

    # Webhook Tools
    mcp.add_tool(webhook.create_webhook)
    mcp.add_tool(webhook.get_webhook)
    mcp.add_tool(webhook.list_webhooks)
    mcp.add_tool(webhook.update_webhook)
    mcp.add_tool(webhook.delete_webhook)

    # Workspace Tools
    mcp.add_tool(workspace.get_workspaces)
    mcp.add_tool(workspace.get_workspace)
    mcp.add_tool(workspace.get_workspace_boards)
    mcp.add_tool(workspace.create_workspace)
    mcp.add_tool(workspace.update_workspace)
    mcp.add_tool(workspace.delete_workspace)

    # Custom Field Tools (Tier 2)
    mcp.add_tool(custom_field.get_board_custom_fields)
    mcp.add_tool(custom_field.create_custom_field)
    mcp.add_tool(custom_field.update_custom_field)
    mcp.add_tool(custom_field.delete_custom_field)
    mcp.add_tool(custom_field.get_card_custom_field_values)
    mcp.add_tool(custom_field.set_custom_field_value_checkbox)
    mcp.add_tool(custom_field.set_custom_field_value_text)
    mcp.add_tool(custom_field.set_custom_field_value_number)
    mcp.add_tool(custom_field.set_custom_field_value_date)
    mcp.add_tool(custom_field.set_custom_field_value_list)
    mcp.add_tool(custom_field.add_custom_field_option)
    mcp.add_tool(custom_field.update_custom_field_option)
    mcp.add_tool(custom_field.delete_custom_field_option)

    # Search Tools (Tier 2)
    mcp.add_tool(search.search_trello)
    mcp.add_tool(search.search_members)

    # Batch Tools (Tier 2)
    mcp.add_tool(batch.batch_get_resources)

    # Export & Template Tools (Tier 2/3)
    mcp.add_tool(export.export_board)
    mcp.add_tool(export.list_organization_exports)
    mcp.add_tool(export.create_organization_export)
    mcp.add_tool(export.create_board_from_template)

    # Advanced Card Tools (Tier 2)
    mcp.add_tool(advanced_card.set_card_due_date)
    mcp.add_tool(advanced_card.set_card_due_complete)
    mcp.add_tool(advanced_card.subscribe_to_card)
    mcp.add_tool(advanced_card.unsubscribe_from_card)
    mcp.add_tool(advanced_card.vote_on_card)
    mcp.add_tool(advanced_card.remove_vote_from_card)
    mcp.add_tool(advanced_card.set_card_start_date)

    # Analytics Tools (Tier 3)
    mcp.add_tool(analytics.get_board_statistics)
    mcp.add_tool(analytics.get_card_cycle_time)
