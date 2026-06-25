"""
Data Transfer Object for adding a comment to a card.
"""

from pydantic import BaseModel, Field, field_validator


class AddCommentPayload(BaseModel):
    """Payload for adding a comment to a card."""

    text: str = Field(..., description="The comment text (required)", min_length=1)

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Validate comment text is not empty or just whitespace."""
        if not v or not v.strip():
            raise ValueError("Comment text cannot be empty or just whitespace")
        return v.strip()

    def to_api_params(self) -> dict:
        """
        Convert payload to API parameters format.

        Returns:
            Dictionary of parameters for the Trello API
        """
        return {"text": self.text}
