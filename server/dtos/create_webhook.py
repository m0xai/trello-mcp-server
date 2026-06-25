"""
Data Transfer Object for creating a webhook.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CreateWebhookPayload(BaseModel):
    """Payload for creating a webhook."""

    callback_url: str = Field(
        ..., description="The URL to receive webhook events (required)"
    )
    id_model: str = Field(
        ..., description="The ID of the model to watch (board, card, or list) (required)"
    )
    description: Optional[str] = Field(
        None, description="Description of the webhook"
    )
    active: bool = Field(
        default=True, description="Whether the webhook is active"
    )

    @field_validator("callback_url")
    @classmethod
    def validate_callback_url(cls, v: str) -> str:
        """Validate callback URL format."""
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

    @field_validator("id_model")
    @classmethod
    def validate_id_model(cls, v: str) -> str:
        """Validate model ID format."""
        if not v or len(v) < 10:
            raise ValueError("Invalid model ID format")
        return v

    def to_api_params(self) -> dict:
        """
        Convert payload to API parameters format.

        Returns:
            Dictionary of parameters for the Trello API
        """
        params = {
            "callbackURL": self.callback_url,
            "idModel": self.id_model,
            "active": str(self.active).lower()
        }
        
        if self.description:
            params["description"] = self.description
        
        return params
