"""
MCP tools for custom field operations.
"""

from mcp.server.fastmcp import Context
from server.services.custom_field import CustomFieldService
from server.dtos.create_custom_field import CreateCustomFieldPayload
from server.dtos.set_custom_field_value import SetCustomFieldValuePayload
from server.validators import ValidationService
from server.trello import client

service = CustomFieldService(client)
validator = ValidationService(client)


async def get_board_custom_fields(ctx: Context, board_id: str) -> str:
    """Get all custom fields defined on a board."""
    await validator.validate_board_exists(board_id)
    fields = service.get_board_custom_fields(board_id)
    return f"Found {len(fields)} custom field(s)"


async def create_custom_field(ctx: Context, board_id: str, name: str, field_type: str, pos: str = "bottom") -> str:
    """Create a new custom field on a board."""
    await validator.validate_board_exists(board_id)
    payload = CreateCustomFieldPayload(id_model=board_id, name=name, type=field_type, pos=pos)
    field = service.create_custom_field(payload)
    return f"Created custom field '{field.name}' (ID: {field.id})"


async def update_custom_field(ctx: Context, field_id: str, name: str = None, pos: str = None) -> str:
    """Update a custom field."""
    field = service.update_custom_field(field_id, name=name, pos=pos)
    return f"Updated custom field '{field.name}'"


async def delete_custom_field(ctx: Context, field_id: str) -> str:
    """Delete a custom field."""
    service.delete_custom_field(field_id)
    return f"Deleted custom field {field_id}"


async def get_card_custom_field_values(ctx: Context, card_id: str) -> str:
    """Get all custom field values on a card."""
    await validator.validate_card_exists(card_id)
    items = service.get_card_custom_field_items(card_id)
    return f"Found {len(items)} custom field value(s)"


async def set_custom_field_value_checkbox(ctx: Context, card_id: str, field_id: str, checked: bool) -> str:
    """Set a checkbox custom field value."""
    await validator.validate_card_exists(card_id)
    payload = SetCustomFieldValuePayload(value={"checked": str(checked).lower()})
    service.set_custom_field_value(card_id, field_id, payload)
    return f"Set checkbox field to {checked}"


async def set_custom_field_value_text(ctx: Context, card_id: str, field_id: str, text: str) -> str:
    """Set a text custom field value."""
    await validator.validate_card_exists(card_id)
    payload = SetCustomFieldValuePayload(value={"text": text})
    service.set_custom_field_value(card_id, field_id, payload)
    return f"Set text field to '{text}'"


async def set_custom_field_value_number(ctx: Context, card_id: str, field_id: str, number: float) -> str:
    """Set a number custom field value."""
    await validator.validate_card_exists(card_id)
    payload = SetCustomFieldValuePayload(value={"number": str(number)})
    service.set_custom_field_value(card_id, field_id, payload)
    return f"Set number field to {number}"


async def set_custom_field_value_date(ctx: Context, card_id: str, field_id: str, date: str) -> str:
    """Set a date custom field value."""
    await validator.validate_card_exists(card_id)
    payload = SetCustomFieldValuePayload(value={"date": date})
    service.set_custom_field_value(card_id, field_id, payload)
    return f"Set date field to {date}"


async def set_custom_field_value_list(ctx: Context, card_id: str, field_id: str, option_id: str) -> str:
    """Set a list custom field value."""
    await validator.validate_card_exists(card_id)
    payload = SetCustomFieldValuePayload(id_value=option_id)
    service.set_custom_field_value(card_id, field_id, payload)
    return f"Set list field to option {option_id}"


async def add_custom_field_option(ctx: Context, field_id: str, text: str, color: str = "none", pos: str = "bottom") -> str:
    """Add an option to a list-type custom field."""
    option = service.add_custom_field_option(field_id, text, color, pos)
    return f"Added option '{text}' (ID: {option['id']})"


async def update_custom_field_option(ctx: Context, option_id: str, text: str = None, color: str = None, pos: str = None) -> str:
    """Update a custom field option."""
    service.update_custom_field_option(option_id, text, color, pos)
    return f"Updated option {option_id}"


async def delete_custom_field_option(ctx: Context, option_id: str) -> str:
    """Delete a custom field option."""
    service.delete_custom_field_option(option_id)
    return f"Deleted option {option_id}"
