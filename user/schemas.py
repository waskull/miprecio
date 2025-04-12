from enum import Enum
from typing import Optional
import uuid
from pydantic import BaseModel
from pydantic import BaseModel, Field
from datetime import datetime

class UserModel(BaseModel):
    uid: uuid.UUID
    email: str
    fullname: str
    role: str
    is_verified: bool
    password: str = Field(exclude=True)
    created_at: Optional[datetime]
    update_at: Optional[datetime]

class UserModelIdEmail(BaseModel):
    uid: uuid.UUID
    email: str

class UserEditModel(BaseModel):
    fullname: str = Field(max_length=25)

class UserPasswordEditModel(BaseModel):
    password: str = Field(min_length=6)

class UserCreateModel(BaseModel):
    fullname: str = Field(max_length=25)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "fullname": "Martin Castillo",
                "email": "test@gmail.com",
                "password": "123456",
            }
        }
    }

class Role (Enum):
    user = "user"
    admin = "admin"