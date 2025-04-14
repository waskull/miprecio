from typing import TYPE_CHECKING, List
import uuid

from pydantic import BaseModel, Field

from ..product.model import Product

class CateModel(BaseModel):
    name: str = Field(max_length=100, min_length=2)
    description: str
    uid: uuid.UUID
    products: list[Product]

class CategoryModel(BaseModel):
    name: str = Field(max_length=80, min_length=2)
    description: str
    uid: uuid.UUID