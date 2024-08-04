"""
Authentication endpoints.
"""

import uuid

import pydantic

from . import utils


class UserBase(pydantic.BaseModel):
    """
    Base model for user information.

    Attributes:
        username: The username of the user.
        phone_number: The phone number of the user.
        email: The email address of the user.
        provider: A list of strings representing the providers associated with the user.
    """

    username: str
    phone_number: str
    email: str
    provider: list[str]


class UserInDB(UserBase):
    """
    User model representing a user in the database.

    Attributes:
        _id: The unique identifier for the user.
        password: The hashed password of the user.
    """

    _id: uuid.UUID
    salt: bytes
    password_hash: bytes

    def check_password(self, password: str):
        return utils.verify_password(password.encode("utf-8"), self.password_hash)

    def change_password(self, password: str):
        self.salt = utils.generate_salt()
        self.password_hash = utils.get_password_hash(self.salt, password)


class UserInRegister(UserBase):
    """
    User model for handling user data when registering.

    Attributes:
        password: Unhashed password of the user.
    """

    password: str


class UserInLogin(pydantic.BaseModel):
    email: str
    password: str
