"""
Authentication business logic
"""

from vitaltrack import config
from vitaltrack import database

from . import models


async def get_user(
    db_manager: database.DatabaseManager,
    email: str,
) -> models.UserInDB | None:
    result = await db_manager.db[config.USERS_COLLECTION_NAME].find_one(
        {"email": email}
    )
    if result:
        return models.UserInDB(**result)
