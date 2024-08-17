"""
FastAPI backend application initialization.
"""

from contextlib import asynccontextmanager

import fastapi

from vitaltrack import config
from vitaltrack import core
from vitaltrack import food
from vitaltrack import provider
from vitaltrack import user


# Actions before and after the application begins accepting requests.
# See: https://fastapi.tiangolo.com/advanced/events/?h=#lifespan
@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    # Setup
    core.database.global_db_manager.connect_to_cluster(url=config.MONGO_DB_URL)
    core.database.global_db_manager.connect_to_database(config.MONGO_DB_DATABASE)
    yield
    # Teardown
    core.database.global_db_manager.close_cluster_connection()


app = fastapi.FastAPI(lifespan=lifespan, root_path=config.API_V1_STR)

app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(provider.router, prefix="/provider", tags=["provider"])
app.include_router(food.router, prefix="/food", tags=["food"])
