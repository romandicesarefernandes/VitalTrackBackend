"""
Authentication business logic
"""

from __future__ import annotations


from vitaltrack import config
from vitaltrack import database

from . import models


async def get_user(
    db_manager: database.DatabaseManager,
    email: str,
) -> models.UserInDB | None:
    """
    Retrieves a user from the database by their email address.

    Args:
        db_manager: The database manager instance used to interact with the database.
        email: The email address of the user to retrieve.

    Returns:
        An instance of `models.UserInDB` if a user with the specified email is found,
            otherwise `None` if no user is found.
    """
    result = await db_manager.db[config.USERS_COLLECTION_NAME].find_one(
        {"email": email}
    )
    if result:
        print(f"{result.keys()=}")
        return models.UserInDB(**result)
