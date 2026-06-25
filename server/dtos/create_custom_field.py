"""
Data Transfer Object for creating a custom field.
"""

from typing import Optional, List, Dict

from pydantic import BaseModel, Field, field_validator


class CreateCustomFieldPayload(BaseModel):
    """Payload for creating a custom field on a board."""

    id_model: str = Field(..., description="The ID of the board (required)")
    name: str = Field(..., description="The name of the custom field (required)", min_length=1)
    type: str = Field(..., description="Field type: checkbox, date, list, number, or text (required)")
    pos: Optional[str] = Field("bottom", description="Position: top, bottom, or integer")
    options: Optional[List[Dict]] = Field(None, description="Options for list type fields")

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate custom field type."""
        valid_types = ["checkbox", "date", "list", "number", "text"]
        if v not in valid_types:
            raise ValueError(
                f"Invalid custom field type '{v}'. Must be one of: {', '.join(valid_types)}"
            )
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate field name is not empty."""
        if not v or not v.strip():
            raise ValueError("Custom field name cannot be empty")
        if len(v) > 255:
            raise ValueError("Custom field name must be 255 characters or less")
        return v.strip()

    @field_validator("pos")
    @classmethod
    def validate_pos(cls, v: Optional[str]) -> Optional[str]:
        """Validate position value."""
        if v is None:
            return "bottom"
        if v not in ["top", "bottom"]:
            try:
                int(v)
            except ValueError:
                raise ValueError("Position must be 'top', 'bottom', or a positive integer")
        return v

    def to_api_params(self) -> dict:
        """
        Convert payload to API parameters format.

        Returns:
            Dictionary of parameters for the Trello API
        """
        params = {
            "idModel": self.id_model,
            "modelType": "board",
            "name": self.name,
            "type": self.type,
            "pos": self.pos
        }
        
        if self.options and self.type == "list":
            params["options"] = self.options
        
        return params
