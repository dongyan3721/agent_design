"""Item document model for MongoDB - example CRUD entity."""

from datetime import UTC, datetime
from typing import Optional

from beanie import Document
from pydantic import Field


class Item(Document):
    """Item document model - example entity for demonstrating CRUD operations.

    This is a simple example model. You can use it as a template
    for creating your own models or remove it if not needed.
    """

    title: str = Field(max_length=255)
    description: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    class Settings:
        name = "items"
        indexes = [
            "title",
        ]