from datetime import datetime
from typing import TypedDict

from .serializer import Serializer


class Success(Serializer):
    message: str | None
    success: bool
    id: str | None


class AccessTokenData(TypedDict):
    sub: str  # Subject (user_id)
    jti: str  # JWT ID
    iss: str  # Issuer
    aud: str  # Audiance
    exp: datetime  # Expiration time
    iat: datetime  # Issued at time
    typ: str  # Token type
    orgs: list[str]  # Orgs list
