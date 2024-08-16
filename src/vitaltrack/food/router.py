"""
Food endpoints.py
"""

from __future__ import annotations

from typing import Annotated

import fastapi
import httpx

from vitaltrack import config

from . import schemas

router = fastapi.APIRouter()
user_router = fastapi.APIRouter()


@router.get(
    "/search",
    response_model=schemas.MultipleFoodsInResponse,
    response_model_by_alias=False,
)
async def search(ingredient="", brand=""):
    food_search_url = f"{config.FOOD_DATABASE_PARSER_URL}&ingr={ingredient}&brand{brand}&nutrition-type=logging"
    # TODO: Error handling
    res = httpx.get(food_search_url)
    res_dict = res.json()

    food_list = []

    for food in res_dict["parsed"]:
        food_list.append(schemas.FoodBase(**food["food"]).model_dump())

    return {
        "message": f"food search returned {len(res_dict['parsed'])} items",
        "data": food_list,
    }


@router.post(
    "/nutrients",
    response_model=schemas.NutrientsInResponse,
    response_model_by_alias=False,
)
async def nutrients(
    ingredients: Annotated[schemas.IngredientsInRequest, fastapi.Body(embed=False)]
):
    food_search_url = f"{config.FOOD_DATABASE_NUTRIENTS_URL}"
    # TODO: Error handling
    res = httpx.post(food_search_url, json=ingredients.model_dump(by_alias=True))
    res_dict = res.json()
    # TODO: Edamam doesn't allow multiple ingredients in request?

    return {
        "message": "nutrients queried",
        "data": res_dict,
    }
