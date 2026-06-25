from typing import List, Optional

from pydantic import BaseModel
from server.models.custom_field import TrelloCustomField, TrelloCustomFieldItem, TrelloCustomFieldOption


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


class TrelloWebhook(BaseModel):
    """Model representing a Trello webhook."""

    id: str
    description: str | None = None
    idModel: str
    callbackURL: str
    active: bool
    consecutiveFailures: int | None = None
    firstConsecutiveFailDate: str | None = None


class TrelloAction(BaseModel):
    """Model representing a Trello action (comment, activity)."""

    id: str
    type: str
    date: str
    idMemberCreator: str | None = None
    data: dict | None = None
    memberCreator: dict | None = None


class TrelloAttachment(BaseModel):
    """Model representing a Trello attachment."""

    id: str
    name: str
    url: str
    bytes: int | None = None
    date: str | None = None
    edgeColor: str | None = None
    idMember: str | None = None
    isUpload: bool | None = None
    mimeType: str | None = None
    pos: int | None = None


class TrelloMember(BaseModel):
    """Model representing a Trello member/user."""

    id: str
    fullName: str | None = None
    username: str | None = None
    email: str | None = None
    avatarUrl: str | None = None
    initials: str | None = None
    memberType: str | None = None
    confirmed: bool | None = None


class TrelloOrganization(BaseModel):
    """Model representing a Trello organization/workspace."""

    id: str
    name: str
    displayName: str
    desc: Optional[str] = None
    url: str
    idEnterprise: Optional[str] = None
    prefs: Optional[dict] = None
    memberships: Optional[List[str]] = None
