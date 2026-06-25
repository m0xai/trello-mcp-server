"""
Data Transfer Object for updating a webhook.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UpdateWebhookPayload(BaseModel):
    """Payload for updating a webhook."""

    callback_url: Optional[str] = Field(
        None, description="New callback URL"
    )
    description: Optional[str] = Field(
        None, description="New description"
    )
    active: Optional[bool] = Field(
        None, description="Whether the webhook is active"
    )

    @field_validator("callback_url")
    @classmethod
    def validate_callback_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate callback URL format."""
        if v is None:
            return v
        
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
            raise ValueError("Invalid callback URL format. Must start with http:// or https://")
        return v

    def to_api_params(self) -> dict:
        """
        Convert payload to API parameters format.

        Returns:
            Dictionary of parameters for the Trello API
        """
        params = {}
        
        if self.callback_url is not None:
            params["callbackURL"] = self.callback_url
        if self.description is not None:
            params["description"] = self.description
        if self.active is not None:
            params["active"] = str(self.active).lower()
        
        return params
