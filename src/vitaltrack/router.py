"""
Main application router.
"""

import fastapi

from vitaltrack import auth
from vitaltrack import food


user_router = fastapi.APIRouter(prefix="/user", tags=["user"])
user_router.include_router(auth.user_router)
user_router.include_router(food.user_router)

provider_router = fastapi.APIRouter(prefix="/provider", tags=["provider"])
provider_router.include_router(auth.provider_router)

food_router = fastapi.APIRouter(prefix="/food", tags=["food"])
food_router.include_router(food.food_router)

global_router = fastapi.APIRouter()
global_router.include_router(user_router)
global_router.include_router(provider_router)
global_router.include_router(food_router)
