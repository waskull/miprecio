import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .model import Store
from ..company.model import Company

class StoreService:
    async def get_all_stores(self, session: AsyncSession):  
        stmt = select(Company).where(Company.is_deleted == False).order_by(Company.name)
        result = await session.exec(stmt)
        return result.all()
    
    async def get_stores(self, session: AsyncSession):  
        stmt = select(Store)
        result = await session.exec(stmt)
        return result.all()

    async def get_store_by_id(self, id: uuid.UUID, session: AsyncSession) -> Store:
        statement = select(Store).where(Store.uid == id)
        result = await session.exec(statement)
        store = result.first()
        return store
    
    async def get_store_by_company_id(self, id: uuid.UUID, session: AsyncSession) -> Store:
        statement = select(Company).where(Company.uid == id).where(Company.is_deleted == False).order_by(Company.name)
        result = await session.exec(statement)
        store = result.first()
        store_ = []
        for i in store.store:
            if i.is_deleted == False:
                store_.append(i)
        store.store = store_
        return store
    async def get_store_by_company_product_uid(self, id: uuid.UUID, product_uid: uuid.UUID,  session: AsyncSession) -> Store:
        statement = select(Store).where(Store.company_uid == id).where(Store.product_uid == product_uid)
        result = await session.exec(statement)
        store = result.first()
        return store
    
    async def check_store(self, company_uid: uuid.UUID, product_uid: uuid.UUID, session: AsyncSession) -> Store:
        statement = select(Store).where(Store.company_uid == company_uid).where(Store.product_uid == product_uid)
        result = await session.exec(statement)
        store = result.first()
        return store
    
    async def create_store(self, store: Store, user_data_id: uuid.UUID, session: AsyncSession) -> Store:
        store_data_dict = store.model_dump()
        newstore = Store(**store_data_dict)
        newstore.uid = uuid.uuid4()
        newstore.user_uid = user_data_id
        session.add(newstore)
        await session.commit()
        return store
    
    async def delete_store(self, store: Store, session: AsyncSession) -> None:
        store.is_deleted = True
        session.add(store)
        await session.commit()
        await session.refresh(store)
        return store
    async def enable_store(self, store: Store, session: AsyncSession) -> None:
        store.is_deleted = False
        session.add(store)
        await session.commit()
        await session.refresh(store)
        return store
    
    async def edit_store(self, store: Store, store_data: dict, session: AsyncSession) -> Store:
        store.price = store_data.price
        if store_data.wholesale_price is not None:
            store.wholesale_price = store_data.wholesale_price
        if store_data.discount is not None: 
            store.discount = store_data.discount
        store.product_uid = store_data.product_uid
        store.company_uid = store_data.company_uid
        session.add(store)
        await session.commit()
        await session.refresh(store)
        return store