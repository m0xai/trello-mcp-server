from typing import Any, Dict, List

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


class TrelloMember(BaseModel):
    """Model representing a Trello member."""

    id: str
    fullName: str
    username: str


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
    idMembers: List[str] = []
    dueComplete: bool = False
    cover: Dict[str, Any] | None = None
    subscribed: bool = False
    attachments: List[Dict[str, Any]] = []
