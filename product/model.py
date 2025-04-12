from datetime import date, datetime
from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import TEXT, Column, Field, Relationship, SQLModel

from ..user.model import User

if TYPE_CHECKING:
    from ..user.model import User

class Product(SQLModel, table=True):
    __tablename__ = "products"
    uid: uuid.UUID = Field(uuid.uuid4 ,nullable=False, primary_key=True)
    name: str = Field(TEXT, nullable=False, unique=True, index=True, max_length=80)
    price: float = Field(nullable=False, default=0.0, decimal_places=2, gt=-1)
    description: str = Field(TEXT, nullable=True)
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(nullable=True)
    update_at: datetime = Field(nullable=True)
    createdBy: Optional["User"] = Relationship(back_populates="products", sa_relationship_kwargs={"lazy": "selectin"})
    #reviews: List["Review"] = Relationship(
    #    back_populates="product", sa_relationship_kwargs={"lazy": "selectin"}
    #)
    #tags: List[Product] = Relationship(
    #    link_model=ProductTag,
    #    back_populates="products",
    #    sa_relationship_kwargs={"lazy": "selectin"},
    #)

    def __repr__(self):
        return f"<Producto {self.name}, precio: {self.price}>"

