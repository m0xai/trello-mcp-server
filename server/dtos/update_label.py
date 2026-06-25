"""
Data Transfer Object for updating a label.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UpdateLabelPayload(BaseModel):
    """Payload for updating a label."""

    name: Optional[str] = Field(None, description="New label name")
    color: Optional[str] = Field(None, description="New label color")

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        """Validate label color."""
        if v is None:
            return v
        
        valid_colors = [
            "green", "yellow", "orange", "red", "purple",
            "blue", "sky", "lime", "pink", "black", "null"
        ]
        
        if v not in valid_colors:
            raise ValueError(
                f"Invalid label color '{v}'. Must be one of: {', '.join(valid_colors)}"
            )
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate label name length."""
        if v is not None and len(v) > 16384:
            raise ValueError("Label name must be 16384 characters or less")
        return v

    def to_api_params(self) -> dict:
        """
        Convert payload to API parameters format.

        Returns:
            Dictionary of parameters for the Trello API
        """
        params = {}
        if self.name is not None:
            params["name"] = self.name
        if self.color is not None:
            params["color"] = self.color if self.color != "null" else None
        return params
