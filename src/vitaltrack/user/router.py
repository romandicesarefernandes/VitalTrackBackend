"""
User endpoints.
"""

from __future__ import annotations

import uuid
from typing import Annotated

import fastapi
import pydantic

from vitaltrack import config
from vitaltrack import core
from vitaltrack import food
from vitaltrack import provider

from . import models
from . import schemas
from . import services

router = fastapi.APIRouter()


@router.post("/register", response_model=schemas.UserRegisterResponse)
async def register_user(
    user: schemas.UserInRegister,
    db_manager: core.dependencies.database_manager_dep,
):
    """
    Register a new user in the database.

    Args:
        user: The user data provided in the request body.
            This includes user details such as username, email, etc.
        db_manager: Dependency injection for the database manager
            used to connect to the MongoDB database and perform operations.

    Returns:
        TODO: Add return
    """
    # TODO: Verify user doesn't exist

    # Generate user password hash
    user_in_req_dict = user.model_dump()
    salt = core.utils.generate_salt()
    password_hash = core.utils.get_password_hash(
        user_in_req_dict.pop("password").encode("utf-8"),
        salt,
    )

    # Add Provider relationship
    provider_in_db = await provider.services.get_provider(
        db_manager, {"provider_code": user_in_req_dict["provider_code"]}
    )
    if not provider_in_db:
        raise fastapi.HTTPException(status_code=400, detail="provider code not found")

    new_user = models.UserInDB(
        id=uuid.uuid4(),
        password_hash=password_hash,
        salt=salt,
        provider=[provider_in_db.id],
        **user_in_req_dict,
    )

    result = await db_manager.db[config.USERS_COLLECTION_NAME].insert_one(
        new_user.model_dump(by_alias=True)
    )

    await db_manager.db[config.PROVIDERS_COLLECTION_NAME].update_one(
        {"_id": provider_in_db.id}, {"$addToSet": {"users": new_user.id}}
    )

    # TODO: Verify database save success

    return {
        "message": f"{user_in_req_dict['email']} registered",
        "data": user_in_req_dict,
    }


@router.post("/login", response_model=schemas.UserLoginResponse)
async def login_user(
    user: schemas.UserInLogin,
    db_manager: core.dependencies.database_manager_dep,
):
    """
    Authenticate and login.

    Args:
        user: The user data provided in the request body.
            This includes user details such as username, email, etc.
        db_manager: Dependency injection for the database manager
            used to connect to the MongoDB database and perform operations.

    Returns:
        TODO: Add return
    """
    user_in_req_dict = user.model_dump()

    user_in_db = await services.get_user(
        db_manager, {"email": user_in_req_dict["email"]}
    )
    if not user_in_db or not user_in_db.check_password(user_in_req_dict["password"]):
        raise fastapi.HTTPException(
            status_code=400, detail="incorrect email or password"
        )

    return {"message": "login successful", "data": {}}


@router.post(
    "/profile",
    response_model=schemas.UserProfileResponse,
)
async def profile(
    email: Annotated[pydantic.EmailStr, fastapi.Body(embed=True)],
    db_manager: core.dependencies.database_manager_dep,
):
    user_in_db = await services.get_user(db_manager, {"email": email})

    if not user_in_db:
        raise fastapi.HTTPException(
            status_code=400, detail="incorrect email or password"
        )

    return {
        "message": "",
        "data": user_in_db.model_dump(),
    }


@router.post(
    "/add-food",
    response_model=food.schemas.MultipleFoodIdsInResponse,
)
async def add_food(
    email: Annotated[pydantic.EmailStr, fastapi.Body()],
    food_ids: Annotated[list[str], fastapi.Body()],
    db_manager: core.dependencies.database_manager_dep,
):
    result = await db_manager.db[config.USERS_COLLECTION_NAME].update_one(
        {"email": email}, {"$addToSet": {"foods": {"$each": food_ids}}}
    )

    if result.matched_count == 0:
        raise fastapi.HTTPException(status_code=400, detail="no user with email found")

    return {
        "message": f"{result.modified_count} food(s) added",
        "data": {},
    }
