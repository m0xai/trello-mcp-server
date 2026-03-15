from typing import Literal

from pydantic import BaseModel


class CreateCardPayload(BaseModel):
    """
    Payload for creating a card.

    Attributes:
        name (str): The name of the card. For smart cards (board, link, mirror),
            set this to the URL.
        desc (str): The description of the card.
        closed (bool): Whether the card is closed or not.
        idMembers (str): Comma-separated list of member IDs for the card.
        idList (str): The ID of the list the card is in.
        idLabels (str): Comma-separated list of label IDs for the card.
        idBoard (str): The ID of the board the card is in.
        pos (str | int): The position of the card.
        due (str): The due date of the card in ISO 8601 format.
        start (str): The start date of the card in ISO 8601 format.
        dueComplete (bool): Whether the card is due complete or not.
        subscribed (bool): Whether the card is subscribed or not.
        cardRole (str): The card's display role. Use "board" with a Trello board
            URL as name to render as a board link. Use "link" with an external URL
            (GitHub, YouTube, etc.) to render as a rich link preview. Use "mirror"
            with a Trello card URL to render as a mirrored card. Use "separator"
            to render as a visual divider.
    """

    name: str
    desc: str | None = None
    closed: bool | None = None
    idMembers: str | None = None
    idList: str
    idLabels: str | None = None
    idBoard: str | None = None
    pos: str | None = None
    due: str | None = None
    start: str | None = None
    dueComplete: bool | None = None
    subscribed: bool | None = None
    cardRole: Literal["board", "link", "mirror", "separator"] | None = None
