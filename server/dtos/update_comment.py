"""
Data Transfer Object for updating a comment.
"""

from pydantic import BaseModel, Field, field_validator


class UpdateCommentPayload(BaseModel):
    """Payload for updating a comment."""

    text: str = Field(..., description="The new comment text (required)", min_length=1)

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
