"""
Utils for Provider endpoints.
"""

import asyncio
import random
import string

from vitaltrack import config
from vitaltrack import core


async def generate_provider_code(
    db_manager: core.database.DatabaseManager,
    timeout: int = 5,
) -> str | None:
    async def _generate_code():
        while True:
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            # Check if the generated code already exists
            if not await db_manager.db[config.PROVIDERS_COLLECTION_NAME].find_one(
                {"provider_code": code}
            ):
                return code

    try:
        code = await asyncio.wait_for(_generate_code(), timeout)
        return code
    except asyncio.TimeoutError:
        raise None
