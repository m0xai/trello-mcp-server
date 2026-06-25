"""
Data Transfer Object for setting a custom field value on a card.
"""

from typing import Optional, Any, Dict

from pydantic import BaseModel, Field, field_validator


class SetCustomFieldValuePayload(BaseModel):
    """Payload for setting a custom field value on a card."""

    value: Optional[Dict[str, Any]] = Field(None, description="Value object for the field")
    id_value: Optional[str] = Field(None, description="Option ID for list type fields")

    @field_validator("value")
    @classmethod
    def validate_value(cls, v: Optional[Dict]) -> Optional[Dict]:
        """Validate value structure."""
        if v is None:
            return v
        
        # Value should be a dict with one of: checked, date, text, number
        valid_keys = ["checked", "date", "text", "number"]
        if not any(key in v for key in valid_keys):
            raise ValueError(
                f"Value must contain one of: {', '.join(valid_keys)}"
            )
        
        return v

    def to_api_params(self) -> dict:
        """
        Convert payload to API parameters format.

        Returns:
            Dictionary of parameters for the Trello API
        """
        params = {}
        
        if self.value is not None:
            params["value"] = self.value
        
        if self.id_value is not None:
            params["idValue"] = self.id_value
        
        return params
