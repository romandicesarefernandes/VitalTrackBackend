"""
User business logic
"""

from __future__ import annotations

from typing import Any

from vitaltrack import config
from vitaltrack import core

from . import models


async def get_user(
    db_manager: core.database.DatabaseManager,
    filter: dict[str, Any],
) -> models.UserInDB | None:
    """
    Retrieves a user from the database by their email address.

    Args:
        db_manager: The database manager instance used to interact with the database.
        filter: Filter to query User collection with.

    Returns:
        An instance of `models.UserInDB` if a user with the specified email is found,
            otherwise `None` if no user is found.
    """
    result = await db_manager.db[config.USERS_COLLECTION_NAME].find_one(filter)
    if result:
        return models.UserInDB(**result)
