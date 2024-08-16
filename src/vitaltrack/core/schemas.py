"""
Global schemas for data validation.
"""

from typing import Any

import pydantic


class SchemaBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True, extra="ignore")


class ResponseBase(pydantic.BaseModel):
    message: str
    data: dict[str, Any] = pydantic.Field(...)
