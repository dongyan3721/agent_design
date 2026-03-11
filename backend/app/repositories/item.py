"""Item repository (MongoDB).

Contains database operations for Item entity. Business logic
should be handled by ItemService in app/services/item.py.
"""

from datetime import UTC, datetime

from app.db.models.item import Item


async def get_by_id(item_id: str) -> Item | None:
    """Get item by ID."""
    return await Item.get(item_id)


async def get_multi(
    *,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
) -> list[Item]:
    """Get multiple items with pagination."""
    query = Item.find_all()
    if active_only:
        query = Item.find(Item.is_active == True)  # noqa: E712
    return await query.skip(skip).limit(limit).to_list()


async def create(
    *,
    title: str,
    description: str | None = None,
) -> Item:
    """Create a new item."""
    item = Item(
        title=title,
        description=description,
    )
    await item.insert()
    return item


async def update(
    *,
    db_item: Item,
    update_data: dict,
) -> Item:
    """Update an item."""
    for field, value in update_data.items():
        setattr(db_item, field, value)
    db_item.updated_at = datetime.now(UTC)
    await db_item.save()
    return db_item


async def delete(item_id: str) -> Item | None:
    """Delete an item."""
    item = await get_by_id(item_id)
    if item:
        await item.delete()
    return item