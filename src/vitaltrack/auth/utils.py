"""
Authentication utility functions.
"""

import bcrypt


def generate_salt() -> bytes:
    return bcrypt.gensalt()


def get_password_hash(password: bytes, salt: bytes) -> bytes:
    return bcrypt.hashpw(password, salt)


def verify_password(password_to_check: bytes, password_hash: bytes) -> bytes:
    return bcrypt.checkpw(password_to_check, password_hash)
