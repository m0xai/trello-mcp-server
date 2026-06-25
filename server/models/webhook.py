"""
Trello Webhook model.
"""

from typing import Optional

from pydantic import BaseModel


class TrelloWebhook(BaseModel):
    """Represents a Trello webhook."""

    id: str
    description: Optional[str] = None
    idModel: str
    callbackURL: str
    active: bool
    consecutiveFailures: Optional[int] = None
    firstConsecutiveFailDate: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow additional fields from API
