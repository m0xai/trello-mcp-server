"""
Data Transfer Object for attaching a URL to a card.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class AttachUrlPayload(BaseModel):
    """Payload for attaching a URL to a card."""

    url: str = Field(..., description="The URL to attach (required)")
    name: Optional[str] = Field(None, description="Display name for the attachment")

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL format."""
        import re
        url_pattern = re.compile(
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or IP
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        if not url_pattern.match(v):
            raise ValueError("Invalid URL format. Must start with http:// or https://")
        return v

    def to_api_params(self) -> dict:
        """
        Convert payload to API parameters format.

        Returns:
            Dictionary of parameters for the Trello API
        """
        params = {"url": self.url}
        if self.name:
            params["name"] = self.name
        return params
