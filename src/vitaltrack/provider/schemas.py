"""
Provider schemas for data validation.
"""

from __future__ import annotations

from typing import Any

import pydantic

from vitaltrack import core


class ProviderBase(core.schemas.SchemaBase):
    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    email: pydantic.EmailStr = pydantic.Field(...)
    phone_number: str = pydantic.Field(...)


class ProviderInRegister(ProviderBase):
    password: str = pydantic.Field(...)


class ProviderInLogin(core.schemas.SchemaBase):
    email: pydantic.EmailStr = pydantic.Field(...)
    password: str = pydantic.Field(...)


class ProviderRegisterResponse(core.schemas.ResponseBase):
    class _ProviderWithCode(ProviderBase):
        provider_code: str = pydantic.Field(...)

    data: _ProviderWithCode = pydantic.Field(...)


class ProviderLoginResponse(core.schemas.ResponseBase):
    data: dict[str, Any] = pydantic.Field(...)
