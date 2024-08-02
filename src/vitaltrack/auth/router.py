"""
Authentication endpoints.
"""

import uuid
from typing import Annotated

import fastapi

from vitaltrack import config
from vitaltrack import dependencies

from . import models

router = fastapi.APIRouter()


@router.post("/login")
async def login_user():
    """
    Authenticate and login.
    """
    return {"log": "in"}


@router.post("/register")
async def register_user(
    user: Annotated[models.UserInRequest, fastapi.Body(embed=True)],
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
    new_user = models.UserInDB(
        _id=uuid.uuid4(), password="test_password", **user.model_dump()
    )

    await db_manager.connect_to_database(config.MONGO_DB_DATABASE)
    result = await db_manager.db[config.USERS_COLLECTION_NAME].insert_one(
        new_user.model_dump()
    )

    return {"result": str(result)}
