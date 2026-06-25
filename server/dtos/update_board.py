"""
Data Transfer Object for updating a board.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UpdateBoardPayload(BaseModel):
    """Payload for updating an existing Trello board."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=16384, description="Board name"
    )
    desc: Optional[str] = Field(None, max_length=16384, description="Board description")
    closed: Optional[bool] = Field(None, description="Archive or unarchive the board")
    id_organization: Optional[str] = Field(
        None, description="Move board to this organization/workspace"
    )
    prefs_permission_level: Optional[str] = Field(
        None, description="Board visibility: private, org, or public"
    )
    prefs_voting: Optional[str] = Field(
        None, description="Voting permissions: disabled, members, observers, org, public"
    )
    prefs_comments: Optional[str] = Field(
        None,
        description="Comment permissions: disabled, members, observers, org, public",
    )
    prefs_self_join: Optional[bool] = Field(
        None, description="Allow users to join the board themselves"
    )
    prefs_card_covers: Optional[bool] = Field(
        None, description="Show card cover images"
    )

    @field_validator("prefs_permission_level")
    @classmethod
    def validate_permission_level(cls, v: Optional[str]) -> Optional[str]:
        """Validate permission level is one of the allowed values."""
        if v is None:
            return v
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

    def to_api_params(self) -> dict:
        """
        Convert payload to API parameters format.

        Returns:
            Dictionary of parameters for the Trello API
        """
        params = {}
        
        if self.name is not None:
            params["name"] = self.name
        if self.desc is not None:
            params["desc"] = self.desc
        if self.closed is not None:
            params["closed"] = self.closed
        if self.id_organization is not None:
            params["idOrganization"] = self.id_organization
        if self.prefs_permission_level is not None:
            params["prefs/permissionLevel"] = self.prefs_permission_level
        if self.prefs_voting is not None:
            params["prefs/voting"] = self.prefs_voting
        if self.prefs_comments is not None:
            params["prefs/comments"] = self.prefs_comments
        if self.prefs_self_join is not None:
            params["prefs/selfJoin"] = self.prefs_self_join
        if self.prefs_card_covers is not None:
            params["prefs/cardCovers"] = self.prefs_card_covers
        
        return params
