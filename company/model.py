from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import TEXT, Boolean, Field, Relationship, SQLModel
if TYPE_CHECKING:
    from ..user.model import User
    from ..store.model import Store

class Company(SQLModel, table=True):
    __tablename__ = "companies"
    uid: uuid.UUID = Field(uuid.uuid4 ,nullable=False, primary_key=True)
    name: str = Field(TEXT, nullable=False, unique=True, index=True, max_length=100)
    description: str = Field(TEXT, nullable=True)
    is_deleted: bool = Field(default=False)
    user_uid: uuid.UUID = Field(default=None, foreign_key="users.uid")
    partner_uid: uuid.UUID = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(nullable=True)
    deleted_at: datetime = Field(nullable=True)
    update_at: datetime = Field(nullable=True)
    user: "User" = Relationship(
         back_populates="user_registered_companies", 
         sa_relationship_kwargs={"lazy": "selectin", "foreign_keys": "Company.user_uid"}
    )
    partner: "User"  = Relationship(
        back_populates="companies", 
        sa_relationship_kwargs={"lazy": "selectin", "foreign_keys": "Company.partner_uid"})
    store: list["Store"] = Relationship(
        back_populates="company",
        #sa_relationship={RelationshipProperty("Product", primaryjoin="Product.createdBy == User.uid", uselist=True)},
        sa_relationship_kwargs={"lazy": "selectin", "uselist": True},
        cascade_delete=True
    )

    def __repr__(self):
        return f"<Compañia {self.name}>"

