import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, Field

from ..user.schemas import UserModel
from ..category.schemas import CategoryModel

class ProductCreateModel(BaseModel):
    name: str = Field(max_length=100, min_length=2)  
    price: float = Field(gt=-1)
    description: str
    user_uid: Optional[uuid.UUID] = Field(default=None)
    category_uid: Optional[uuid.UUID] = Field(default=None)

class ProductUModel(ProductCreateModel):
    uid: uuid.UUID

class ProductEditPriceModel(BaseModel):
    price: float = Field(gt=-1)

class ProductEditModel(ProductEditPriceModel):
    name: str = Field(max_length=100, min_length=2) 
    description: str

class ProductModel(ProductCreateModel):
    createdBy: Optional[UserModel]
    category: Optional[CategoryModel]

class ProductBasicModel(BaseModel):
    uid: uuid.UUID
    name: str = Field(max_length=100, min_length=2)
    description: str

class ProductModelWithCategory(ProductCreateModel):
    user_uid: Optional[uuid.UUID] = Field(exclude=True)
    createdBy: Optional[UserModel]
    uid: uuid.UUID
    category: Optional[CategoryModel]

class UserProductsModel(UserModel):
    #books: List[Book]
    #reviews: List[ReviewModel]
    pass