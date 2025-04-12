import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, Field

from ..user.schemas import UserModel

class ProductCreateModel(BaseModel):
    name: str
    price: float
    description: str
    user_uid: Optional[uuid.UUID] = Field(default=None)

class ProductEditPriceModel(BaseModel):
    price: float

class ProductEditModel(ProductEditPriceModel):
    name: str
    description: str

class ProductModel(BaseModel):
    name: str
    price: float
    description: str
    user_uid: uuid.UUID
    createdBy: Optional[UserModel]

class UserProductsModel(UserModel):
    #books: List[Book]
    #reviews: List[ReviewModel]
    pass