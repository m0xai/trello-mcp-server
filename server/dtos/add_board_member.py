"""
Data Transfer Object for adding a member to a board.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class AddBoardMemberPayload(BaseModel):
    """Payload for adding a member to a board."""

    email: str = Field(
        ..., description="Email address of the member to add (required)"
    )
    type: str = Field(
        default="normal",
        description="Member type: normal, admin, or observer"
    )
    allow_billable_guest: Optional[bool] = Field(
        None, description="Allow adding as billable guest if not in workspace"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        import re
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if not email_pattern.match(v):
            raise ValueError("Invalid email format")
        return v.lower()

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
        params = {
            "email": self.email,
            "type": self.type
        }
        
        if self.allow_billable_guest is not None:
            params["allowBillableGuest"] = str(self.allow_billable_guest).lower()
        
        return params
