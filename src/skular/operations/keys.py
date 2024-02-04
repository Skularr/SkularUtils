from loguru import logger

from ..rests.keys import get_public_key


class Keys:
    keys: dict[str, str] = {}

    @classmethod
    async def get_key(cls, org_name: str) -> [str, str]:
        if not cls.keys.get(org_name):
            logger.debug("Key not found in cache, getting it from access server...")
            key = await get_public_key(org_name)
            cls.keys[org_name] = key

        return cls.keys[org_name]
