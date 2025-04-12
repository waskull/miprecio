from datetime import datetime, timedelta
import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..user.model import User
from .model import TokenBlacklist
from ..product.model import Product
TOKEN_EXPIRY = 3600

class AuthService:
    async def get_token(self, token: str, session: AsyncSession):
        statement = select(TokenBlacklist).where(TokenBlacklist.token == token)
        result = await session.exec(statement)
        blacklist_token = result.first()
        return blacklist_token is not None
    
    async def add_token_to_blocklist(self, jti: str, session: AsyncSession):
        print(jti)
        uid = uuid.uuid4()
        token = TokenBlacklist(uid = uid, token=jti)
        session.add(token)
        await session.commit()