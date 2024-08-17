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


@router.get(
    "/search",
    # response_model=schemas.MultipleFoodsInResponse,
    # response_model_by_alias=False,
)
async def search(foods: Annotated[schemas.FoodInSearch, fastapi.Body(embed=False)]):
    # TODO: Error handling

    url = f"{config.OPENFOODFACTS_URL}/search"
    query_params = {"categories_tags_en": "pizza", "fields": "code,product_name,brands"}
    res = httpx.get(
        url,
        params=query_params,
        headers={"User-Agent": config.OPENFOODFACTS_USER_AGENT},
    )
    res_dict = res.json()

    # return {
    #     "message": f"food search returned {len(res_dict['parsed'])} items",
    #     "data": food_list,
    # }
    return {
        "message": "",
        "data": res_dict,
    }


# @router.post(
#     "/nutrients",
#     response_model=schemas.NutrientsInResponse,
#     response_model_by_alias=False,
# )
# async def nutrients(
#     ingredients: Annotated[schemas.IngredientsInRequest, fastapi.Body(embed=False)]
# ):
#     food_search_url = f"{config.FOOD_DATABASE_NUTRIENTS_URL}"
#     # TODO: Error handling
#     res = httpx.post(food_search_url, json=ingredients.model_dump(by_alias=True))
#     res_dict = res.json()
#     # TODO: Edamam doesn't allow multiple ingredients in request?

#     return {
#         "message": "nutrients queried",
#         "data": res_dict,
#     }
