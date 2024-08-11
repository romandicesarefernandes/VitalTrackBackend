from typing import Any

import pydantic


class ResponseBase(pydantic.BaseModel):
    message: str
    data: dict[str, Any] = pydantic.Field(...)
