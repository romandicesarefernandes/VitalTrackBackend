"""
FastAPI backend application initialization.
"""

from contextlib import asynccontextmanager

import fastapi

from vitaltrack import auth
from vitaltrack import food
from vitaltrack import config
from vitaltrack import database


# Actions before and after the application begins accepting requests.
# See: https://fastapi.tiangolo.com/advanced/events/?h=#lifespan
@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    # Setup
    database.global_db_manager.connect_to_cluster(url=config.MONGO_DB_URL)
    database.global_db_manager.connect_to_database(config.MONGO_DB_DATABASE)
    yield
    # Teardown
    database.global_db_manager.close_cluster_connection()


app = fastapi.FastAPI(lifespan=lifespan)

app.include_router(auth.user_router, tags=["user"])
app.include_router(auth.provider_router, tags=["provider"])
app.include_router(food.router, tags=["food"])
