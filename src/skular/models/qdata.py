from typing import TypedDict


class QData(TypedDict):
    id: str
    producer: str
    topic: str
    content: dict
    action: str
    org: str
