"""
Authentication endpoints.
"""

import uuid
from typing import Annotated

import fastapi

from vitaltrack import config
from vitaltrack import dependencies

from . import models
from . import services
from . import utils

router = fastapi.APIRouter()


@router.post("/login")
async def login_user(
    user: models.UserInLogin,
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
    return "login successful"


@router.post("/register")
async def register_user(
    user: Annotated[models.UserInRegister, fastapi.Body(embed=True)],
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
        _id=uuid.uuid4(), password_hash=password_hash, salt=salt, **user_in_req_dict
    )

    result = await db_manager.db[config.USERS_COLLECTION_NAME].insert_one(
        new_user.model_dump()
    )

    # TODO: Verify database save success

    return f"{user_in_req_dict['email']} registered"
