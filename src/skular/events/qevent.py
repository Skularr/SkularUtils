import asyncio
import json
from asyncio import Queue
from os import getenv

from httpx import AsyncClient
from loguru import logger

from .model import QData


class Event:
    _stopped = False
    _connected = False
    __stop_success = Queue()

    @classmethod
    def start_loop(cls):
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(cls.listen(), loop)

    @classmethod
    async def listen(cls):
        headers = {
            'x-token': getenv('TOKEN')
        }
        topic = 'skular'
        logger.debug(f"Listening to events on topic: {topic}..")
        cls._connected = True
        while not cls._stopped:
            async with AsyncClient() as client:
                res = await client.get(f'{getenv("QUEUE_SERVICE_URL")}/listen/{topic}', headers=headers)

            success = res.status_code == 201
            if success:
                data: QData = await res.json()
                logger.debug(f"Event recieved successfully....\n{json.dumps(data, indent=4)}")

        await cls.__stop_success.put(True)
        logger.debug(f"Event listener of topic: {topic} is stopped...")

    @classmethod
    async def send(cls, topic: str, action: str, organization: str, content: dict) -> bool:
        data = {
            "poducer": "skular",
            "topic": topic,
            "content": content,
            "action": action,
            "org": organization
        }

        headers = {
            'x-token': getenv('TOKEN')
        }

        async with AsyncClient() as client:
            res = await client.post(f'{getenv("QUEUE_SERVICE_URL")}/create', json=data, headers=headers)

        return res.status_code == 201

    @classmethod
    async def stop(cls):
        cls._stopped = True
        if not cls._connected:
            logger.debug("Event listener is already stopped...")
            return False
        logger.debug("Stopping event listener...")
        return await cls.__stop_success.get()
