"""
Data Transfer Object for creating a board.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CreateBoardPayload(BaseModel):
    """Payload for creating a new Trello board."""

    name: str = Field(..., min_length=1, max_length=16384, description="Board name")
    desc: Optional[str] = Field(
        None, max_length=16384, description="Board description"
    )
    id_organization: Optional[str] = Field(
        None, description="ID of the organization/workspace to create the board in"
    )
    default_lists: bool = Field(
        True, description="Automatically add default lists (To Do, Doing, Done)"
    )
    default_labels: bool = Field(
        True, description="Automatically add default labels"
    )
    prefs_permission_level: str = Field(
        default="private",
        description="Board visibility: private, org, or public",
    )
    prefs_voting: Optional[str] = Field(
        None, description="Voting permissions: disabled, members, observers, org, public"
    )
    prefs_comments: Optional[str] = Field(
        None,
        description="Comment permissions: disabled, members, observers, org, public",
    )

    @field_validator("prefs_permission_level")
    @classmethod
    def validate_permission_level(cls, v: str) -> str:
        """Validate permission level is one of the allowed values."""
        valid_levels = ["private", "org", "public"]
        if v not in valid_levels:
            raise ValueError(
                f"Permission level must be one of: {', '.join(valid_levels)}"
            )
        return v

    @field_validator("prefs_voting")
    @classmethod
    def validate_voting(cls, v: Optional[str]) -> Optional[str]:
        """Validate voting permission is one of the allowed values."""
        if v is None:
            return v
        valid_values = ["disabled", "members", "observers", "org", "public"]
        if v not in valid_values:
            raise ValueError(f"Voting must be one of: {', '.join(valid_values)}")
        return v

    @field_validator("prefs_comments")
    @classmethod
    def validate_comments(cls, v: Optional[str]) -> Optional[str]:
        """Validate comments permission is one of the allowed values."""
        if v is None:
            return v
        valid_values = ["disabled", "members", "observers", "org", "public"]
        if v not in valid_values:
            raise ValueError(f"Comments must be one of: {', '.join(valid_values)}")
        return v
