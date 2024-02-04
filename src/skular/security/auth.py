from os import getenv

import jwt
from loguru import logger

from ..operations.keys import Keys


def decode_token(token: str, public_key: str) -> [bool, str]:
    try:
        decoded_payload = jwt.decode(
            token, public_key, algorithms=[getenv("ALGORITHM")],
            issuer="access", audience="skular"
        )
        return True, decoded_payload
    except jwt.ExpiredSignatureError:
        return False, "Token has expired"
    except Exception as e:
        error = str(e)
        logger.error(error)
        return False, error


async def get_token_data(access_token, org) -> [bool, str | dict]:
    public = await Keys.get_key(org)
    success, data = decode_token(access_token, public)
    return success, data
