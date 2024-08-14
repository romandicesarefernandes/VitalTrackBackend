"""
Authentication models interactions with MongoDB.

'InDB' is add to class names to add more distinction from schemas.
"""

from __future__ import annotations

import uuid

import pydantic

from vitaltrack import models

from . import utils


class AuthMixin(pydantic.BaseModel):
    salt: bytes = pydantic.Field(...)
    password_hash: bytes = pydantic.Field(...)

    def check_password(self, password: str):
        return utils.verify_password(password.encode("utf-8"), self.password_hash)

    def change_password(self, password: str):
        self.salt = utils.generate_salt()
        self.password_hash = utils.get_password_hash(self.salt, password)


class UserInDB(models.ModelInDBBase, AuthMixin):
    """
    User collection for Mongo.

    Attributes:
        id: The unique identifier for the user.
        first_name: The first name of the user.
        last_name: The last name of the user.
        username: The username of the user.
        phone_number: The phone number of the user.
        email: The email address of the user.
        provider: A list of strings representing the providers associated with the user.
    """

    id: uuid.UUID = pydantic.Field(alias="_id")
    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    username: str = pydantic.Field(...)
    phone_number: str = pydantic.Field(...)
    email: pydantic.EmailStr = pydantic.Field(...)
    provider: list[ProviderInDB] = pydantic.Field(default=[])
    foods: list[str] = pydantic.Field(default=[])


class ProviderInDB(models.ModelInDBBase, AuthMixin):
    id: uuid.UUID = pydantic.Field(alias="_id")
    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    email: pydantic.EmailStr = pydantic.Field(...)
    phone_number: str = pydantic.Field(...)
    users: list[UserInDB] = pydantic.Field(default=None)
