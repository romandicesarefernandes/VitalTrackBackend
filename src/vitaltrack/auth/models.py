"""
Authentication endpoints.
"""

import uuid

import pydantic


class UserBase(pydantic.BaseModel):
    """
    Base model for user information.

    Attributes:
        username: The username of the user.
        phone_number: The phone number of the user.
        email: The email address of the user.
        provider: A list of strings representing the providers associated with the user.
    """

    username: str
    phone_number: str
    email: str
    provider: list[str]


class UserInDB(UserBase):
    """
    User model representing a user in the database.

    Attributes:
        _id: The unique identifier for the user.
        password: The hashed password of the user.
    """

    _id: uuid.UUID
    password: str


class UserInRequest(UserBase):
    """
    User model for handling user data in requests.
    """

    pass
