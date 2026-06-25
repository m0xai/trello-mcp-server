"""
Data Transfer Object for creating a workspace/organization.
"""

import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CreateWorkspacePayload(BaseModel):
    """Payload for creating a Trello workspace/organization."""

    display_name: str = Field(
        ..., min_length=1, max_length=16384, description="Workspace display name (required)"
    )
    desc: Optional[str] = Field(
        None, max_length=16384, description="Workspace description"
    )
    name: Optional[str] = Field(
        None, description="Workspace short name (used in URL, lowercase alphanumeric and underscores only)"
    )
    website: Optional[str] = Field(None, description="Workspace website URL")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate workspace name format (lowercase alphanumeric and underscores, min 3 chars)."""
        if v is None:
            return v
        if not re.match(r"^[a-z0-9_]{3,}$", v):
            raise ValueError(
                "Workspace name must be at least 3 characters and contain only lowercase letters, numbers, and underscores"
            )
        return v

    @field_validator("website")
    @classmethod
    def validate_website(cls, v: Optional[str]) -> Optional[str]:
        """Validate website URL format."""
        if v is None:
            return v
        
        url_pattern = re.compile(
            r"^https?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        
        if not url_pattern.match(v):
            raise ValueError("Website must be a valid HTTP or HTTPS URL")
        return v

    def to_api_params(self) -> dict:
        """
        Convert payload to API parameters format.

        Returns:
            Dictionary of parameters for the Trello API
        """
        params = {"displayName": self.display_name}
        
        if self.desc is not None:
            params["desc"] = self.desc
        if self.name is not None:
            params["name"] = self.name
        if self.website is not None:
            params["website"] = self.website
        
        return params
