"""
Authentication schemas for data validation.
"""

from __future__ import annotations

import pydantic

from vitaltrack import schemas


class UserBase(schemas.SchemaBase):
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


class UserResponse(schemas.ResponseBase): ...


class UserInRegister(UserBase):
    """
    User model for handling user data when registering.

    Attributes:
        password: Unhashed password of the user.
    """

    password: str = pydantic.Field(...)


class UserInLogin(schemas.SchemaBase):
    """
    User model for handling user data when at login.

    Attributes:
        email: Email of the user.
        password: Unhashed password of the user.
    """

    email: pydantic.EmailStr = pydantic.Field(...)
    password: str = pydantic.Field(...)


class ProviderBase(schemas.SchemaBase):
    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    email: pydantic.EmailStr = pydantic.Field(...)
    phone_number: str = pydantic.Field(...)
    # users: list[UserInDB] = pydantic.Field(default=None)
