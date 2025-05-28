import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .model import Product

class ProductService:
    async def get_all_products(self, session: AsyncSession) -> list[Product]:
        stmt = select(Product)
        result = await session.exec(stmt)
        return result.all()
    async def get_top_products(self, session: AsyncSession) -> list[Product]:
        stmt = select(Product).limit(5).order_by(Product.update_at.desc())
        result = await session.exec(stmt)
        return result.all()
    async def get_product_by_name(self, name: str, session: AsyncSession) -> Product:
        statement = select(Product).where(Product.name == name)
        result = await session.exec(statement)
        product = result.first()
        return product
    
    async def get_product_by_id(self, id: uuid.UUID, session: AsyncSession) -> Product:
        statement = select(Product).where(Product.uid == id)
        result = await session.exec(statement)
        product = result.first()
        return product

    async def product_exists(self, name, session: AsyncSession) -> bool:
        product = await self.get_product_by_name(name, session)
        return True if product is not None else False

    async def create_product(self, product_data: Product, session: AsyncSession) -> Product:
        product_data_dict = product_data.model_dump()
        new_product = Product(**product_data_dict)
        new_product.uid = uuid.uuid4()
        session.add(new_product)
        await session.commit()
        return new_product


    async def update_product(self, product:Product , product_data: dict,session:AsyncSession) -> Product:
        for k, v in product_data.items():
            setattr(product, k, v)

        await session.commit()
        return product
    
    async def edit_product(self, product: Product, product_data: Product, session: AsyncSession) -> Product:
        product.name = product_data.name
        product.price = product_data.price
        product.description =product_data.description
        session.add(product)
        await session.commit()
        return product

    async def delete_product(self, id: uuid.UUID, session: AsyncSession):
        statement = select(Product).where(Product.uid == id)
        result = await session.exec(statement)
        product = result.first()
        await session.delete(product)
        await session.commit()