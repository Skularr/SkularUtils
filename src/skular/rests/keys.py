from os import getenv

from httpx import AsyncClient
from loguru import logger


async def get_public_key(org_id: str) -> str:
    try:
        async with AsyncClient() as client:
            r = await client.get(f'{getenv("ACCESS_SERVICE_URL")}/v1/public/key', params={'org_id': org_id})

        return r.json()
    except Exception as e:
        logger.error(str(e))
        return ""
