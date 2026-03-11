"""User repository (MongoDB).

Contains only database operations. Business logic (password hashing,
validation) is handled by UserService in app/services/user.py.
"""

from app.db.models.user import User


async def get_by_id(user_id: str) -> User | None:
    """Get user by ID."""
    return await User.get(user_id)


async def get_by_email(email: str) -> User | None:
    """Get user by email."""
    return await User.find_one(User.email == email)

async def get_multi(
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    """Get multiple users with pagination."""
    return await User.find_all().skip(skip).limit(limit).to_list()


async def create(
    *,
    email: str,
    hashed_password: str | None,
    full_name: str | None = None,
    is_active: bool = True,
    is_superuser: bool = False,
    role: str = "user",) -> User:
    """Create a new user.

    Note: Password should already be hashed by the service layer.
    """
    user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        is_active=is_active,
        is_superuser=is_superuser,
        role=role,    )
    await user.insert()
    return user


async def update(
    *,
    db_user: User,
    update_data: dict,
) -> User:
    """Update a user.

    Note: If password needs updating, it should already be hashed.
    """
    for field, value in update_data.items():
        setattr(db_user, field, value)

    await db_user.save()
    return db_user


async def delete(user_id: str) -> User | None:
    """Delete a user."""
    user = await get_by_id(user_id)
    if user:
        await user.delete()
    return user