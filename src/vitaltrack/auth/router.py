"""
Authentication endpoints.
"""

from __future__ import annotations

import uuid
from typing import Annotated

import fastapi

from vitaltrack import config
from vitaltrack import dependencies

from . import models
from . import schemas
from . import services
from . import utils

user_router = fastapi.APIRouter()
provider_router = fastapi.APIRouter()


@user_router.post("/register", response_model=schemas.UserRegisterResponse)
async def register_user(
    user: schemas.UserInRegister,
    db_manager: dependencies.database_manager_dep,
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
    salt = utils.generate_salt()
    password_hash = utils.get_password_hash(
        user_in_req_dict.pop("password").encode("utf-8"),
        salt,
    )

    # Add Provider relationship
    provider_in_db = await services.get_provider(
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


@user_router.post("/login", response_model=schemas.UserLoginResponse)
async def login_user(
    user: schemas.UserInLogin,
    db_manager: dependencies.database_manager_dep,
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


@provider_router.post("/register", response_model=schemas.ProviderRegisterResponse)
async def register_provider(
    provider: schemas.ProviderInRegister,
    db_manager: dependencies.database_manager_dep,
):
    # TODO: Verify provider doesn't exist

    # Generate user password hash
    provider_in_req_dict = provider.model_dump()
    salt = utils.generate_salt()
    password_hash = utils.get_password_hash(
        provider_in_req_dict.pop("password").encode("utf-8"),
        salt,
    )

    # Generate unique provider code
    provider_code = await utils.generate_provider_code(db_manager)

    new_provider = models.ProviderInDB(
        id=uuid.uuid4(),
        password_hash=password_hash,
        salt=salt,
        provider_code=provider_code,
        **provider_in_req_dict,
    )

    result = await db_manager.db[config.PROVIDERS_COLLECTION_NAME].insert_one(
        new_provider.model_dump(by_alias=True)
    )

    # TODO: Verify database save success

    return {
        "message": f"{provider_in_req_dict['email']} registered",
        "data": {"provider_code": provider_code, **provider_in_req_dict},
    }


@provider_router.post("/login", response_model=schemas.ProviderLoginResponse)
async def login_provider(
    provider: schemas.UserInLogin,
    db_manager: dependencies.database_manager_dep,
):
    provider_in_req_dict = provider.model_dump()

    provider_in_db = await services.get_provider(
        db_manager, {"email": provider_in_req_dict["email"]}
    )
    if not provider_in_db or not provider_in_db.check_password(
        provider_in_req_dict["password"]
    ):
        raise fastapi.HTTPException(
            status_code=400, detail="incorrect email or password"
        )

    return {"message": "login successful", "data": {}}
