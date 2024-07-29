"""
FastAPI backend application initialization.
"""

import fastapi

from vitaltrack import api

app = fastapi.FastAPI()

app.include_router(api.api_router)
