"""
Application dependenices.

See: https://fastapi.tiangolo.com/tutorial/dependencies/
"""

from typing import Annotated

import fastapi

from vitaltrack import database

database_manager_dep = Annotated[
    database.DatabaseManager, fastapi.Depends(database.get_database_manager)
]

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="token")
token_scheme_dep = Annotated[str, fastapi.Depends(oauth2_scheme)]
