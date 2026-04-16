"""
User helper classes.
module: src/util/models/user.py
"""

from pydantic import BaseModel, EmailStr, Field
from api.src.util.models.base_db_model import BaseDbModel


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr


class UserArguments(User):
    password: str = Field(..., min_length=8)


class NewUser(User):
    password_hash: str


class UserModel(BaseDbModel):
    __tablename__: str = "users"
    user_id: int
    username: str
    email: EmailStr
    password_hash: str
    permission_level: int


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)
