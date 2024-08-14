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

FOOD_DATABASE_API_KEY = "6db423635db56cd0fdf46cce1c5edfb3"
FOOD_DATABASE_API_ID = "750c3845"
FOOD_DATABASE_PARSER_URL = f"https://api.edamam.com/api/food-database/v2/parser?app_id={FOOD_DATABASE_API_ID}&app_key={FOOD_DATABASE_API_KEY}"
FOOD_DATABASE_NUTRIENTS_URL = f"https://api.edamam.com/api/food-database/v2/nutrients?app_id={FOOD_DATABASE_API_ID}&app_key={FOOD_DATABASE_API_KEY}"

USERS_COLLECTION_NAME = "users"
PROVIDERS_COLLECTION_NAME = "providers"
FOOD_COLLECTION_NAME = "food"
