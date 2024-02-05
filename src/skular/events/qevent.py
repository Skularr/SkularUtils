import asyncio
import json
from asyncio import Queue
from os import getenv
from typing import Callable

from httpx import AsyncClient
from loguru import logger

from ..models.qdata import QData


class Event:
    _stopped = False
    _connected = False
    __stop_success = Queue()

    @classmethod
    def start_loop(cls, topic: str, event_handler_class: Callable):
        """
        Starts the event loop and registers it with the given topic and pass incoming data
        to the event_handler_class and execute the event handler asyncronusly.
        """
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(cls.listen(topic, event_handler_class), loop)

    @classmethod
    async def listen(cls, topic, event_handler_class):
        headers = {
            'x-token': getenv('TOKEN')
        }
        logger.debug(f"Listening to events on topic: {topic}..")
        cls._connected = True
        while not cls._stopped:
            async with AsyncClient() as client:
                res = await client.get(f'{getenv("QUEUE_SERVICE_URL")}/listen/{topic}', headers=headers)

            success = res.status_code == 201
            if success:
                data: QData = await res.json()
                logger.debug(f"Event recieved successfully....\n{json.dumps(data, indent=4)}")
                operation = event_handler_class(data)
                await operation()

        await cls.__stop_success.put(True)
        logger.debug(f"Event listener of topic: {topic} is stopped...")

    @classmethod
    async def send(cls, producer: str, topic: str, action: str, organization: str, content: dict) -> bool:
        data = {
            "producer": producer,
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
