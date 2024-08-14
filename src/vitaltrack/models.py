"""
Global models interactions with MongoDB.

'InDB' is add to class names to add more distinction from schemas.
"""

import pydantic


class ModelInDBBase(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True)
