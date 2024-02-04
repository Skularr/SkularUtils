from datetime import datetime
from typing import TypedDict


class AccessTokenData(TypedDict):
    sub: str  # Subject (user_id)
    jti: str  # JWT ID
    iss: str  # Issuer
    aud: str  # Audiance
    exp: datetime  # Expiration time
    iat: datetime  # Issued at time
    typ: str  # Token type
    orgs: list[str]  # Orgs list
