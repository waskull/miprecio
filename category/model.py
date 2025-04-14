from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional
import uuid

from sqlmodel import TEXT, Column, Field, Relationship, SQLModel
if TYPE_CHECKING:
    from ..product.model import Product

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    uid: uuid.UUID = Field(uuid.uuid4 ,nullable=False, primary_key=True)
    name: str = Field(TEXT, nullable=False, unique=True, index=True, max_length=80)
    description: str = Field(TEXT, nullable=True)
    created_at: datetime = Field(nullable=True)
    update_at: datetime = Field(nullable=True)
    products: list["Product"] = Relationship(
        back_populates="category",
        #sa_relationship_kwargs={"lazy": "selectin", "uselist": True, "order_by": "Product.name"},
        cascade_delete=True,
    )

    def __repr__(self):
        return f"<Categoria: {self.name}>"

