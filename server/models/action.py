"""
Trello Action model (for comments and activity).
"""

from typing import Optional

from pydantic import BaseModel


class TrelloAction(BaseModel):
    """Represents a Trello action (comment, activity, etc.)."""

    id: str
    type: str
    date: str
    idMemberCreator: Optional[str] = None
    data: Optional[dict] = None
    memberCreator: Optional[dict] = None
    
    class Config:
        extra = "allow"  # Allow additional fields from API
