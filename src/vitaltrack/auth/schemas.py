"""
Authentication schemas for data validation.
"""

from __future__ import annotations

from typing import Any

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


class UserRegisterResponse(schemas.ResponseBase):
    data: UserBase = pydantic.Field(...)


class UserInRegister(UserBase):
    """
    User model for handling user data when registering.

    Attributes:
        password: Unhashed password of the user.
    """

    password: str = pydantic.Field(...)
    provider_code: str = pydantic.Field(...)


class UserInLogin(schemas.SchemaBase):
    """
    User model for handling user data when at login.

    Attributes:
        email: Email of the user.
        password: Unhashed password of the user.
    """

    email: pydantic.EmailStr = pydantic.Field(...)
    password: str = pydantic.Field(...)


class UserLoginResponse(schemas.ResponseBase):
    data: dict[str, Any] = pydantic.Field(...)


class ProviderBase(schemas.SchemaBase):
    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    email: pydantic.EmailStr = pydantic.Field(...)
    phone_number: str = pydantic.Field(...)


class ProviderInRegister(ProviderBase):
    password: str = pydantic.Field(...)


class ProviderInLogin(schemas.SchemaBase):
    email: pydantic.EmailStr = pydantic.Field(...)
    password: str = pydantic.Field(...)


class ProviderRegisterResponse(schemas.ResponseBase):
    class _ProviderWithCode(ProviderBase):
        provider_code: str = pydantic.Field(...)

    data: _ProviderWithCode = pydantic.Field(...)


class ProviderLoginResponse(schemas.ResponseBase):
    data: dict[str, Any] = pydantic.Field(...)
