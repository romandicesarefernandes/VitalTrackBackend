"""
REST API initialization.
"""

import fastapi

from .routes import router

api_router = fastapi.APIRouter()
api_router.include_router(router)
