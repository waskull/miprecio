from typing import TYPE_CHECKING, Optional
import uuid
from pydantic import BaseModel

from ..user.schemas import UserCompanyModel

from ..product.schemas import ProductBasicModel

if TYPE_CHECKING:
    from ..company.schemas import CompanyModel

class StoreCreateModel(BaseModel):
    product_uid: uuid.UUID
    company_uid: uuid.UUID
    is_deleted: bool = None
    price: float
    wholesale_price: Optional[float]
    discount: Optional[int]

class StoreDeleteModel(BaseModel):
    product_uid: uuid.UUID

class StoreModel(StoreCreateModel):
    uid: uuid.UUID

class StoreCompanyModel(BaseModel):
    price: float
    wholesale_price: float
    discount: int
    createdBy: Optional[UserCompanyModel]   
    product: Optional[ProductBasicModel]
