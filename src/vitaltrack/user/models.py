"""
User models interactions with MongoDB.

'InDB' is add to class names to add more distinction from schemas.
"""

from __future__ import annotations

import uuid

import pydantic

from vitaltrack import core


class UserInDB(core.models.ModelInDBBase, core.models.AuthMixin):
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
    conditions: list[str] = pydantic.Field(...)
    provider: list[uuid.UUID] = pydantic.Field(default=[])
    foods: list[str] = pydantic.Field(default=[])
