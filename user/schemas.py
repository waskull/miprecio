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

class UserCompanyModel(BaseModel):
    uid: uuid.UUID
    email: str
    fullname: str

class UserModelIdEmail(BaseModel):
    uid: uuid.UUID
    email: str

class UserEditModel(BaseModel):
    fullname: str = Field(max_length=50)

class UserPasswordEditModel(BaseModel):
    old_password: str = Field(min_length=6)
    newpassword: str = Field(min_length=6)
    confirm_newpassword: str = Field(min_length=6)

class UserCreateModel(BaseModel):
    fullname: str = Field(max_length=50, min_length=2)
    email: str = Field(max_length=45, min_length=5)
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
    partner = "socio"