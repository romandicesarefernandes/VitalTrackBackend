"""
Provider models interactions with MongoDB.

'InDB' is add to class names to add more distinction from schemas.
"""

from __future__ import annotations

import uuid

import pydantic

from vitaltrack import core


class ProviderInDB(core.models.ModelInDBBase, core.models.AuthMixin):
    id: uuid.UUID = pydantic.Field(alias="_id")
    first_name: str = pydantic.Field(...)
    last_name: str = pydantic.Field(...)
    email: pydantic.EmailStr = pydantic.Field(...)
    phone_number: str = pydantic.Field(...)
    provider_code: str = pydantic.Field(...)
    users: list[uuid.UUID] = pydantic.Field(default=[])
