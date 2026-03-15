from typing import List

from pydantic import BaseModel


class TrelloBoard(BaseModel):
    """Model representing a Trello board."""

    id: str
    name: str
    desc: str | None = None
    closed: bool = False
    idOrganization: str | None = None
    url: str


class TrelloList(BaseModel):
    """Model representing a Trello list."""

    id: str
    name: str
    closed: bool = False
    idBoard: str
    pos: float


class TrelloLabel(BaseModel):
    """Model representing a Trello label."""
    
    id: str
    name: str
    color: str | None = None


class TrelloComment(BaseModel):
    """Model representing a Trello comment (action of type commentCard)."""

    id: str
    idMemberCreator: str
    type: str
    date: str
    data: dict
    memberCreator: dict | None = None


class TrelloAttachment(BaseModel):
    """Model representing a Trello card attachment."""

    id: str
    name: str
    url: str
    bytes: int | None = None
    mimeType: str | None = None
    isUpload: bool = False
    date: str
    edgeColor: str | None = None
    pos: float | None = None


class TrelloCard(BaseModel):
    """Model representing a Trello card."""

    id: str
    name: str
    desc: str | None = None
    closed: bool = False
    idList: str
    idBoard: str
    url: str
    pos: float
    labels: List[TrelloLabel] = []
    due: str | None = None
