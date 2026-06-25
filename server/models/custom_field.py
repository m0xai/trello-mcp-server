"""
Model for Trello Custom Field.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class TrelloCustomFieldOption(BaseModel):
    """Represents an option in a list-type custom field."""
    
    id: str = Field(..., description="The ID of the option")
    id_custom_field: str = Field(..., description="The ID of the custom field", alias="idCustomField")
    value: Dict[str, str] = Field(..., description="The value object containing text")
    color: str = Field(..., description="The color of the option")
    pos: float = Field(..., description="The position of the option")

    class Config:
        populate_by_name = True


class TrelloCustomField(BaseModel):
    """Represents a Trello custom field definition."""
    
    id: str = Field(..., description="The ID of the custom field")
    id_model: str = Field(..., description="The ID of the board", alias="idModel")
    model_type: str = Field(..., description="The type of model (board)", alias="modelType")
    field_group: Optional[str] = Field(None, description="The field group identifier", alias="fieldGroup")
    name: str = Field(..., description="The name of the custom field")
    pos: float = Field(..., description="The position of the custom field")
    type: str = Field(..., description="The type of the custom field")
    options: Optional[List[TrelloCustomFieldOption]] = Field(None, description="Options for list type fields")
    display: Optional[Dict[str, Any]] = Field(None, description="Display settings")

    class Config:
        populate_by_name = True


class TrelloCustomFieldItem(BaseModel):
    """Represents a custom field value on a card."""
    
    id: str = Field(..., description="The ID of the custom field item")
    id_custom_field: str = Field(..., description="The ID of the custom field", alias="idCustomField")
    id_model: str = Field(..., description="The ID of the card", alias="idModel")
    model_type: str = Field(..., description="The type of model (card)", alias="modelType")
    value: Optional[Dict[str, Any]] = Field(None, description="The value of the custom field")
    id_value: Optional[str] = Field(None, description="The ID of the selected option for list fields", alias="idValue")

    class Config:
        populate_by_name = True
