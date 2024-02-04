from os import getenv

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class Database:
    client: AsyncIOMotorClient = None

    @classmethod
    async def connect(cls):
        cls.client = AsyncIOMotorClient(getenv("MONGODB_URL"))

    @classmethod
    async def disconnect(cls):
        cls.client.close()


async def get_database(db_name: str) -> AsyncIOMotorDatabase:
    client = Database.client
    database: AsyncIOMotorDatabase = client[db_name]
    return database
