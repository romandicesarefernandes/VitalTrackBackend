"""
Food schemas for data validation.
"""

from __future__ import annotations

import pydantic

from typing import Any
from typing import Optional

from vitaltrack import schemas


class FoodBase(schemas.SchemaBase):
    food_id: str = pydantic.Field(alias="foodId")
    uri: Optional[pydantic.HttpUrl] = pydantic.Field(default=None)
    label: Optional[str] = pydantic.Field(default=None)
    known_as: Optional[str] = pydantic.Field(alias="knownAs", default=None)
    nutrients: Optional[dict[str, Any]] = pydantic.Field(default=None)
    brand: Optional[str] = pydantic.Field(default=None)
    category: Optional[str] = pydantic.Field(default=None)
    category_label: Optional[str] = pydantic.Field(alias="categoryLabel", default=None)
    content_label: Optional[str] = pydantic.Field(
        alias="foodContentsLabel", default=None
    )
    image: Optional[str] = pydantic.Field(default=None)
    serving_sizes: Optional[dict[str, Any]] = pydantic.Field(
        alias="servingSizes", default=None
    )
    measure: Optional[dict[str, Any]] = pydantic.Field(default=None)
    servings_per_container: Optional[float] = pydantic.Field(
        alias="servingsPerContainer", default=None
    )


class MultipleFoodIdsInResponse(schemas.ResponseBase): ...


class FoodInResponse(schemas.ResponseBase):
    data: FoodBase = pydantic.Field(...)


class MultipleFoodsInResponse(schemas.ResponseBase):
    data: list[FoodBase] = pydantic.Field(...)


class IngredientBase(schemas.SchemaBase):
    quantity: int = pydantic.Field(...)
    measure_uri: str = pydantic.Field(alias="measureURI")
    qualifiers: list[str] = pydantic.Field(...)
    food_id: str = pydantic.Field(alias="foodId")


class IngredientsInRequest(pydantic.BaseModel):
    ingredients: list[IngredientBase] = pydantic.Field(...)


class NutrientsInResponse(schemas.ResponseBase):
    data: dict[str, Any] = pydantic.Field(...)
