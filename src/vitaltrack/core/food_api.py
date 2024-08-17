"""
API objects and utilities for accessing food APIs.
"""

import openfoodfacts

from vitaltrack import config


OPENFOODFACTS_ENV_MAP = {
    "org": openfoodfacts.Environment.org,
    "net": openfoodfacts.Environment.net,
}

openfoodfacts_api = openfoodfacts.API(
    user_agent=config.OPENFOODFACTS_USER_AGENT,
    username=config.OPENFOODFACTS_USERNAME,
    password=config.OPENFOODFACTS_USERNAME,
    country=openfoodfacts.Country.us,
    flavor=openfoodfacts.Flavor.off,
    version=openfoodfacts.APIVersion.v2,
    environment=OPENFOODFACTS_ENV_MAP.get(
        config.OPENFOODFACTS_ENV, openfoodfacts.Environment.net
    ),
)
