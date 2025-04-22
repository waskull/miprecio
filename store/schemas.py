from typing import Optional
import uuid
from pydantic import BaseModel

from ..user.schemas import UserCompanyModel

from ..product.schemas import ProductBasicModel


class StoreCreateModel(BaseModel):
    product_uid: uuid.UUID
    company_uid: uuid.UUID
    price: float
    wholesale_price: Optional[float]
    discount: Optional[int]

class StoreModel(StoreCreateModel):
    uid: uuid.UUID

class StoreCompanyModel(BaseModel):
    price: float
    wholesale_price: float
    discount: int
    createdBy: Optional[UserCompanyModel]
    product: Optional[ProductBasicModel]
