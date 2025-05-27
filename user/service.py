import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from .schemas import Role, UserCreateModel

from .model import User
from ..auth.utils import generate_passwd_hash

class UserService:
    async def get_all_users(self, session: AsyncSession) -> list[User]:
        stmt = select(User).options(selectinload(User.products)).where(User.role is not Role.admin.value)
        result = await session.exec(stmt)
        return result.all()
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user
    
    async def get_user_by_id(self, id: uuid.UUID, session: AsyncSession):
        statement = select(User).where(User.uid == id)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False
    async def user_exists_by_id(self, user_exists_by_id, session: AsyncSession):
        user = await self.get_user_by_id(user_exists_by_id, session)
        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession, is_partner: bool = False):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.uid = uuid.uuid4()
        if is_partner: new_user.role = Role.partner.value
        else: new_user.role = Role.user.value
        new_user.password = generate_passwd_hash(user_data_dict["password"])
        session.add(new_user)
        await session.commit()
        return new_user
    
    async def create_partner(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.uid = uuid.uuid4()
        new_user.role = Role.partner.value
        new_user.password = generate_passwd_hash(user_data_dict["password"])
        session.add(new_user)
        await session.commit()
        return new_user


    async def update_user(self, user:User , user_data: dict,session:AsyncSession):
        for k, v in user_data.items():
            setattr(user, k, v)

        await session.commit()
        return user

    async def edit_user(self, user:User , user_data: dict, session: AsyncSession) -> User:
        user.name = user_data.name
        user.price = user_data.price
        user.description =user_data.description
        session.add(user)
        await session.commit()
        return user
    
    async def edit_user_password(self, user:User , formpassword: str, session: AsyncSession) -> User:
        newpassword = generate_passwd_hash(formpassword)
        user.password = newpassword
        session.add(user)
        await session.commit()
        return user

    async def delete_user(self, id: uuid.UUID, session: AsyncSession):
        print("ID: ", id)
        statement = select(User).where(User.uid == id)
        result = await session.exec(statement)
        user = result.first()
        print("user: ",user)
        await session.delete(user)
        await session.commit()