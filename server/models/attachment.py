"""
Trello Attachment model.
"""

from typing import Optional

from pydantic import BaseModel


class TrelloAttachment(BaseModel):
    """Represents a Trello card attachment."""

    id: str
    name: str
    url: str
    bytes: Optional[int] = None
    date: Optional[str] = None
    edgeColor: Optional[str] = None
    idMember: Optional[str] = None
    isUpload: Optional[bool] = None
    mimeType: Optional[str] = None
    pos: Optional[int] = None
    previews: Optional[list] = None
    
    class Config:
        extra = "allow"  # Allow additional fields from API
