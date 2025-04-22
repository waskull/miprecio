import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from .model import Category
from ..product.model import Product

class CategoryService:
    async def get_all_categories(self, session: AsyncSession):
        stmt = select(Category).options(selectinload(Category.products)).order_by(Category.name)
        result = await session.exec(stmt)
        return result.all()
    async def get_category_by_name(self, name: str, session: AsyncSession) -> Category:
        statement = select(Category).options(selectinload(Category.products)).where(Category.name == name)
        result = await session.exec(statement)
        category = result.first()
        return category
    async def get_category_by_id(self, id: uuid.UUID, session: AsyncSession) -> Category:
        statement = select(Category).options(selectinload(Category.products)).where(Category.uid == id)
        result = await session.exec(statement)
        category = result.first()
        return category
    
    async def create_category(self, category: Category, session: AsyncSession) -> Category:
        category_data_dict = category.model_dump()
        newcategory = Category(**category_data_dict)
        newcategory.name = newcategory.name.capitalize()
        newcategory.uid = uuid.uuid4()
        if newcategory.description is not None:
            newcategory.description = newcategory.description.capitalize()
        session.add(newcategory)
        await session.commit()
        await session.refresh(newcategory)
        return newcategory
    
    async def delete_category(self, id: uuid.UUID, session: AsyncSession) -> None:
        statement = select(Category).where(Category.uid == id)
        result = await session.exec(statement)
        category = result.first()
        await session.delete(category)
        await session.commit()
        return
    
    async def edit_category(self, category: Category, category_data: dict, session: AsyncSession) -> Category:
        category.name = category_data.name.capitalize()
        category.description = category_data.description
        if category_data.description is not None:
            category.description = category_data.description.capitalize()
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category