"""
Authentication utility functions.
"""

import bcrypt


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
