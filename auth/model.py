from datetime import datetime
import uuid

from sqlmodel import TEXT, Field, SQLModel


class TokenBlacklist(SQLModel, table=True):
    __tablename__ = "blacklist"
    uid: uuid.UUID = Field(uuid.uuid4, nullable=False, primary_key=True)
    token: str = Field(TEXT, nullable=False)
    created_at: datetime = Field(nullable=True)
    update_at: datetime = Field(nullable=True)
    expiracy: datetime = Field(nullable=True)

    def __repr__(self):
        return f"<Token: {self.token}>"