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

router = fastapi.APIRouter(prefix="/auth")


@router.post("/login", response_model=schemas.UserResponse)
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

    user_in_db = await services.get_user(db_manager, user_in_req_dict["email"])
    if not user_in_db or not user_in_db.check_password(user_in_req_dict["password"]):
        raise fastapi.HTTPException(
            status_code=400, detail="incorrect email or password"
        )

    return {"message": "login successful", "data": {}}


@router.post("/register", response_model=schemas.UserResponse)
async def register_user(
    user: Annotated[schemas.UserInRegister, fastapi.Body(embed=True)],
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

    new_user = models.UserInDB(
        id=uuid.uuid4(),
        password_hash=password_hash,
        salt=salt,
        **user_in_req_dict,
    )

    result = await db_manager.db[config.USERS_COLLECTION_NAME].insert_one(
        new_user.model_dump(by_alias=True)
    )

    # TODO: Verify database save success

    return {"message": f"{user_in_req_dict['email']} registered", "data": {}}
