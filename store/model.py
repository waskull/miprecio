from datetime import date, datetime
from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from ..user.model import User
    from ..product.model import Product
    from ..company.model import Company

class Store(SQLModel, table=True):
    __tablename__ = "stores"
    uid: uuid.UUID = Field(uuid.uuid4 ,nullable=False, primary_key=True)
    price: float = Field(nullable=False, default=0.00, decimal_places=2, gt=-1)
    wholesale_price: Optional[float] = Field(nullable=True, default=0.00, decimal_places=2, gt=-1)
    discount: Optional[int] = Field(nullable=True, default=0, gt=-1, lt=100)
    user_uid: uuid.UUID = Field(default=None, foreign_key="users.uid", exclude=True)
    product_uid: uuid.UUID = Field(default=None, foreign_key="products.uid", exclude=True)
    company_uid: uuid.UUID = Field(default=None, foreign_key="companies.uid", exclude=True)
    is_deleted: bool = Field(default=False, nullable=True)
    created_at: datetime = Field(nullable=True)
    update_at: datetime = Field(nullable=True)
    product: "Product" = Relationship(
        back_populates="store", 
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    createdBy: "User" = Relationship(back_populates="stores", sa_relationship_kwargs={"lazy": "selectin"})
    company: "Company" = Relationship(back_populates="store", sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self):
        return f"<Producto {self.name}, Compañia: {self.company.name}, Precio: {self.price}>"

