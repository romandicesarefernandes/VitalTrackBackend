"""
REST API endpoints.
"""

import fastapi

router = fastapi.APIRouter()


@router.get("/")
def root():
    return {"hello": "world"}
