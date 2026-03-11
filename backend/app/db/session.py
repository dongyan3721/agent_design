"""Async MongoDB database session."""

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

client: AsyncIOMotorClient | None = None
_beanie_initialized = False


async def init_db() -> AsyncIOMotorDatabase:
    """Initialize MongoDB client and Beanie document models."""
    global client, _beanie_initialized

    if client is None:
        client = AsyncIOMotorClient(settings.MONGO_URL)

    db = client[settings.MONGO_DB]

    if not _beanie_initialized:
        from app.db.models.conversation import Conversation, Message, ToolCall
        from app.db.models.item import Item
        from app.db.models.user import User

        await init_beanie(
            database=db,
            document_models=[User, Item, Conversation, Message, ToolCall],
        )
        _beanie_initialized = True

    return db


async def get_db_session() -> AsyncIOMotorDatabase:
    """Get MongoDB database instance."""
    return await init_db()


async def close_db() -> None:
    """Close MongoDB connection."""
    global client, _beanie_initialized
    if client is not None:
        client.close()
        client = None
    _beanie_initialized = False
