from typing import TypedDict


class QData(TypedDict):
    id: str
    poducer: str
    topic: str
    content: dict
    action: str
    org: str
