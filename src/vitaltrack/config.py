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

OPENFOODFACTS_URL = "https://world.openfoodfacts.net/api/v2"
OPENFOODFACTS_USER_AGENT = "VitalTrackHealth/0.0 (danielfwilliams@protonmail.com)"
OPENFOODFACTS_USERNAME = os.getenv("OPENFOODFACTS_USERNAME")
OPENFOODFACTS_PASSWORD = os.getenv("OPENFOODFACTS_PASSWORD")
OPENFOODFACTS_ENV = os.getenv("OPENFOODFACTS_ENV")


USERS_COLLECTION_NAME = "users"
PROVIDERS_COLLECTION_NAME = "providers"
FOOD_COLLECTION_NAME = "food"
