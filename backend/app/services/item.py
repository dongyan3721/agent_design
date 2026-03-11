"""Item service (MongoDB).

Contains business logic for item operations. Uses ItemRepository for database access.
"""

from app.core.exceptions import NotFoundError
from app.db.models.item import Item
from app.repositories import item_repo
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """Service for item-related business logic.

    This is an example service demonstrating the service layer pattern.
    Services contain business logic and use repositories for database operations.
    """

    async def get_by_id(self, item_id: str) -> Item:
        """Get item by ID.

        Raises:
            NotFoundError: If item does not exist.
        """
        item = await item_repo.get_by_id(item_id)
        if not item:
            raise NotFoundError(
                message="Item not found",
                details={"item_id": item_id},
            )
        return item

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False,
    ) -> list[Item]:
        """Get multiple items with pagination."""
        return await item_repo.get_multi(skip=skip, limit=limit, active_only=active_only)

    async def create(self, item_in: ItemCreate) -> Item:
        """Create a new item."""
        return await item_repo.create(
            title=item_in.title,
            description=item_in.description,
        )

    async def update(self, item_id: str, item_in: ItemUpdate) -> Item:
        """Update an item.

        Raises:
            NotFoundError: If item does not exist.
        """
        item = await self.get_by_id(item_id)
        update_data = item_in.model_dump(exclude_unset=True)
        return await item_repo.update(db_item=item, update_data=update_data)

    async def delete(self, item_id: str) -> Item:
        """Delete an item.

        Raises:
            NotFoundError: If item does not exist.
        """
        item = await item_repo.delete(item_id)
        if not item:
            raise NotFoundError(
                message="Item not found",
                details={"item_id": item_id},
            )
        return item