"""
Data Transfer Object for updating a board member's role.
"""

from pydantic import BaseModel, Field, field_validator


class UpdateBoardMemberPayload(BaseModel):
    """Payload for updating a board member's role."""

    type: str = Field(
        ..., description="New member type: normal, admin, or observer (required)"
    )

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate member type."""
        valid_types = ["normal", "admin", "observer"]
        if v not in valid_types:
            raise ValueError(
                f"Invalid member type '{v}'. Must be one of: {', '.join(valid_types)}"
            )
        return v

    def to_api_params(self) -> dict:
        """
        Convert payload to API parameters format.

        Returns:
            Dictionary of parameters for the Trello API
        """
        return {"type": self.type}
