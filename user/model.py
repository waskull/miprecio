from datetime import datetime
from typing import TYPE_CHECKING, List
import uuid
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import TEXT, Column, Field, Relationship, SQLModel

from ..user.schemas import Role

if TYPE_CHECKING:
    from ..product.model import Product
    from ..store.model import Store
    from ..company.model import Company

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
    products: list["Product"] = Relationship(
        back_populates="createdBy",
        #sa_relationship={RelationshipProperty("Product", primaryjoin="Product.createdBy == User.uid", uselist=True)},
        sa_relationship_kwargs={"lazy": "selectin"},
        cascade_delete=True
    )
    stores: list["Store"] = Relationship(
        back_populates="createdBy",
        #sa_relationship={RelationshipProperty("Product", primaryjoin="Product.createdBy == User.uid", uselist=True)},
        sa_relationship_kwargs={"lazy": "selectin"},
        cascade_delete=True
    )
    user_registered_companies: list["Company"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin", "foreign_keys": "[Company.user_uid]"},
        cascade_delete=True
    )
    companies: list["Company"] = Relationship(
        back_populates="partner",
        #sa_relationship={RelationshipProperty("Product", primaryjoin="Product.createdBy == User.uid", uselist=True)},
        sa_relationship_kwargs={"lazy": "selectin", "foreign_keys": "[Company.partner_uid]"},
        cascade_delete=True
    )

    def __repr__(self):
        return f"<Usuario: {self.fullname}>"