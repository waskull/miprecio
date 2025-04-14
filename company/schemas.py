from typing import Optional, TYPE_CHECKING
import uuid

from pydantic import BaseModel
from sqlmodel import Field
from ..user.schemas import UserModel


class CompanyCreateModel(BaseModel):
    name: str = Field(max_length=100, min_length=2)  
    price: float = Field(gt=-1, decimal_places=2)
    description: str
    user_uid: Optional[uuid.UUID]
    partner_uid: Optional[uuid.UUID]

class CompanyModel(BaseModel):
    uid: uuid.UUID
    name: str
    description: str
    user_uid: Optional[uuid.UUID] = Field(exclude=True)
    partner_uid: Optional[uuid.UUID] = Field(exclude=True)
    partner: Optional[UserModel]
    user: Optional[UserModel]