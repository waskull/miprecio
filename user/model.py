from datetime import datetime
from typing import TYPE_CHECKING, List
import uuid
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import TEXT, Column, Field, Relationship, SQLModel

from ..user.schemas import Role
from ..category.model import Category

if TYPE_CHECKING:
    from ..product.model import Product
    from ..category.model import Category

class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(uuid.uuid4, nullable=False, primary_key=True)
    email: str
    fullname: str
    role: str = Field(Role.user, nullable=False)
    is_verified: bool = Field(default=False)
    password: str = Field(TEXT, nullable=False, exclude=True)
    created_at: datetime = Field(nullable=True)
    update_at: datetime = Field(nullable=True)
    products: List["Product"] = Relationship(
        back_populates="createdBy",
        #sa_relationship={RelationshipProperty("Product", primaryjoin="Product.createdBy == User.uid", uselist=True)},
        sa_relationship_kwargs={"lazy": "selectin"},
        cascade_delete=True
    )
    
    """
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    ) """

    def __repr__(self):
        return f"<Usuario: {self.fullname}>"