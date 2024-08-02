"""
Global config variables.
"""

import os

import dotenv


API_V1_STR = "/api/v1"

dotenv.load_dotenv()

MONGO_DB_USER = os.getenv("MONGO_DB_USER")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")

MONGO_DB_URL = (
    f"mongodb+srv://{MONGO_DB_USER}:{MONGO_DB_PASSWORD}@vitaltrack.l9rwqw3.mongodb.net"
)
MONGO_DB_DATABASE = os.getenv("MONGO_DB_DATABASE")

MIN_CONNECTIONS_COUNT = 10
MAX_CONNECTIONS_COUNT = 10

USERS_COLLECTION_NAME = "users"
