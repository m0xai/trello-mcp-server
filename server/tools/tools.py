"""
This module contains tools for managing Trello boards, lists, and cards.
"""

from mcp.types import ToolAnnotations

from server.tools import board, card, checklist, list


def register_tools(mcp):
    """Register tools with the MCP server."""
    # Board Tools (read-only)
    mcp.add_tool(
        board.get_board,
        annotations=ToolAnnotations(
            title="Get Board",
            readOnlyHint=True,
        ),
    )
    mcp.add_tool(
        board.get_boards,
        annotations=ToolAnnotations(
            title="Get Boards",
            readOnlyHint=True,
        ),
    )
    mcp.add_tool(
        board.get_board_labels,
        annotations=ToolAnnotations(
            title="Get Board Labels",
            readOnlyHint=True,
        ),
    )
    mcp.add_tool(
        board.create_board_label,
        annotations=ToolAnnotations(
            title="Create Board Label",
            destructiveHint=True,
        ),
    )

    # List Tools
    mcp.add_tool(
        list.get_list,
        annotations=ToolAnnotations(
            title="Get List",
            readOnlyHint=True,
        ),
    )
    mcp.add_tool(
        list.get_lists,
        annotations=ToolAnnotations(
            title="Get Lists",
            readOnlyHint=True,
        ),
    )
    mcp.add_tool(
        list.create_list,
        annotations=ToolAnnotations(
            title="Create List",
            destructiveHint=True,
        ),
    )
    mcp.add_tool(
        list.update_list,
        annotations=ToolAnnotations(
            title="Update List",
            destructiveHint=True,
        ),
    )
    mcp.add_tool(
        list.delete_list,
        annotations=ToolAnnotations(
            title="Delete List",
            destructiveHint=True,
        ),
    )

    # Card Tools
    mcp.add_tool(
        card.get_card,
        annotations=ToolAnnotations(
            title="Get Card",
            readOnlyHint=True,
        ),
    )
    mcp.add_tool(
        card.get_cards,
        annotations=ToolAnnotations(
            title="Get Cards",
            readOnlyHint=True,
        ),
    )
    mcp.add_tool(
        card.create_card,
        annotations=ToolAnnotations(
            title="Create Card",
            destructiveHint=True,
        ),
    )
    mcp.add_tool(
        card.update_card,
        annotations=ToolAnnotations(
            title="Update Card",
            destructiveHint=True,
        ),
    )
    mcp.add_tool(
        card.delete_card,
        annotations=ToolAnnotations(
            title="Delete Card",
            destructiveHint=True,
        ),
    )

    # Checklist Tools
    mcp.add_tool(
        checklist.get_checklist,
        annotations=ToolAnnotations(
            title="Get Checklist",
            readOnlyHint=True,
        ),
    )
    mcp.add_tool(
        checklist.get_card_checklists,
        annotations=ToolAnnotations(
            title="Get Card Checklists",
            readOnlyHint=True,
        ),
    )
    mcp.add_tool(
        checklist.create_checklist,
        annotations=ToolAnnotations(
            title="Create Checklist",
            destructiveHint=True,
        ),
    )
    mcp.add_tool(
        checklist.update_checklist,
        annotations=ToolAnnotations(
            title="Update Checklist",
            destructiveHint=True,
        ),
    )
    mcp.add_tool(
        checklist.delete_checklist,
        annotations=ToolAnnotations(
            title="Delete Checklist",
            destructiveHint=True,
        ),
    )
    mcp.add_tool(
        checklist.add_checkitem,
        annotations=ToolAnnotations(
            title="Add Checkitem",
            destructiveHint=True,
        ),
    )
    mcp.add_tool(
        checklist.update_checkitem,
        annotations=ToolAnnotations(
            title="Update Checkitem",
            destructiveHint=True,
        ),
    )
    mcp.add_tool(
        checklist.delete_checkitem,
        annotations=ToolAnnotations(
            title="Delete Checkitem",
            destructiveHint=True,
        ),
    )
