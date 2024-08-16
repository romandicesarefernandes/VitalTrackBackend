"""
FastAPI backend application initialization.
"""

from contextlib import asynccontextmanager

import fastapi

from vitaltrack import config
from vitaltrack import database
from vitaltrack import router


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

app.include_router(router.global_router)
