"""
Trello Member model.
"""

from typing import Optional

from pydantic import BaseModel


class TrelloMember(BaseModel):
    """Represents a Trello member/user."""

    id: str
    fullName: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    avatarUrl: Optional[str] = None
    initials: Optional[str] = None
    memberType: Optional[str] = None
    confirmed: Optional[bool] = None
    
    class Config:
        extra = "allow"  # Allow additional fields from API
