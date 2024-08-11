"""
Authentication endpoints.
"""

from __future__ import annotations

import uuid

import pydantic

from . import utils


class UserBase(pydantic.BaseModel):
    """
    Base model for user information.

    Attributes:
        first_name: The first name of the user.
        last_name: The last name of the user.
        username: The username of the user.
        phone_number: The phone number of the user.
        email: The email address of the user.
        provider: A list of strings representing the providers associated with the user.
    """

    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    username: str = pydantic.Field(...)
    phone_number: str = pydantic.Field(...)
    email: pydantic.EmailStr = pydantic.Field(...)


class UserInDB(UserBase):
    """
    User model representing a user in the database.

    Attributes:
        _id: The unique identifier for the user.
        password: The hashed password of the user.
    """

    model_config = pydantic.ConfigDict(populate_by_name=True)

    id: uuid.UUID = pydantic.Field(alias="_id")
    salt: bytes = pydantic.Field(...)
    password_hash: bytes = pydantic.Field(...)
    provider: list[ProviderInDB] = pydantic.Field(default=[])

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

    password: str = pydantic.Field(...)


class UserInLogin(pydantic.BaseModel):
    """
    User model for handling user data when at login.

    Attributes:
        email: Email of the user.
        password: Unhashed password of the user.
    """

    email: pydantic.EmailStr = pydantic.Field(...)
    password: str = pydantic.Field(...)


class ProviderBase(pydantic.BaseModel):
    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    email: pydantic.EmailStr = pydantic.Field(...)
    phone_number: str = pydantic.Field(...)
    users: list[UserInDB] = pydantic.Field(default=None)


class ProviderInDB(ProviderBase):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    id: uuid.UUID = pydantic.Field(alias="_id")
    salt: bytes = pydantic.Field(...)
    password_hash: bytes = pydantic.Field(...)

    def check_password(self, password: str):
        return utils.verify_password(password.encode("utf-8"), self.password_hash)

    def change_password(self, password: str):
        self.salt = utils.generate_salt()
        self.password_hash = utils.get_password_hash(self.salt, password)
