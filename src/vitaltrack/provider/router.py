"""
Provider endpoints.
"""

from __future__ import annotations

import uuid

import fastapi

from vitaltrack import config
from vitaltrack import core

from . import models
from . import schemas
from . import services
from . import utils


router = fastapi.APIRouter()


@router.post("/register", response_model=schemas.ProviderRegisterResponse)
async def register_provider(
    provider: schemas.ProviderInRegister,
    db_manager: core.dependencies.database_manager_dep,
):
    # TODO: Verify provider doesn't exist

    # Generate provider password hash
    provider_in_req_dict = provider.model_dump()
    salt = core.generate_salt()
    password_hash = core.get_password_hash(
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


@router.post("/login", response_model=schemas.ProviderLoginResponse)
async def login_provider(
    provider: schemas.ProviderInLogin,
    db_manager: core.dependencies.database_manager_dep,
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
