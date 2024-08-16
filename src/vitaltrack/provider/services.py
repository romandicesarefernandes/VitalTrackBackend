"""
Provider business logic
"""

from __future__ import annotations

from typing import Any

from vitaltrack import config
from vitaltrack import core

from . import models


async def get_provider(
    db_manager: core.database.DatabaseManager,
    filter: dict[str, Any],
) -> models.ProviderInDB | None:
    result = await db_manager.db[config.PROVIDERS_COLLECTION_NAME].find_one(filter)
    if result:
        return models.ProviderInDB(**result)
