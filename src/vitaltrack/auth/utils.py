"""
Authentication utility functions.
"""

from __future__ import annotations

import asyncio
import bcrypt
import random
import string

from vitaltrack import config
from vitaltrack import database

from . import services


def generate_salt() -> bytes:
    """
    Generates a salt for use in password hashing.

    Returns:
        A salt value in bytes.
    """
    return bcrypt.gensalt()


def get_password_hash(password: bytes, salt: bytes) -> bytes:
    """
    Hashes a password using a given salt.

    Args:
        password: The password to hash, provided as bytes.
        salt: The salt to use for hashing.

    Returns:
        bytes: The hashed password as bytes.
    """
    return bcrypt.hashpw(password, salt)


def verify_password(password_to_check: bytes, password_hash: bytes) -> bytes:
    """
    Verifies a password against a hashed password.

    Args:
        password_to_check: The password to check, provided as bytes.
        password_hash: The hashed password to compare against.

    Returns:
        True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password_to_check, password_hash)


async def generate_provider_code(
    db_manager: database.DatabaseManager,
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
