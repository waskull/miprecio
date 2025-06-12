from typing import Optional, TYPE_CHECKING
import uuid

from pydantic import BaseModel
from sqlmodel import Field

from ..store.schemas import StoreCompanyModel
from ..user.schemas import UserModel


class CompanyEditModel(BaseModel):
    name: str = Field(max_length=100, min_length=2) 
    description: str

class CompanyCreateModel(CompanyEditModel):
    partner_uid: Optional[uuid.UUID] = None

class CompanyModel(BaseModel):
    uid: uuid.UUID
    name: str
    description: str
    user_uid: Optional[uuid.UUID] = Field(exclude=True)
    partner_uid: Optional[uuid.UUID] = Field(exclude=True)
    partner: Optional[UserModel]
    user: Optional[UserModel]
    
class CompanyStoreModel(BaseModel):
    uid: uuid.UUID
    name: str
    description:str
    partner: Optional[UserModel]
    store: list[StoreCompanyModel]

#class CompanyStoreModel(CompanyModel):
#    stores: list[StoreCompanyModel]
#    partner: Optional[UserModel]