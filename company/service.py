import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .model import Company
from .schemas import CompanyCreateModel

class CompanyService:
    async def get_all_companies(self, session: AsyncSession):
        stmt = select(Company).where(Company.is_deleted == False).order_by(Company.name)
        result = await session.exec(stmt)
        return result.all()
    async def get_company_by_name(self, name: str, session: AsyncSession) -> Company:
        statement = select(Company).where(Company.name == name)
        result = await session.exec(statement)
        company = result.first()
        return company
    async def get_company_by_id(self, id: uuid.UUID, session: AsyncSession) -> Company:
        statement = select(Company).where(Company.uid == id)
        result = await session.exec(statement)
        company = result.first()
        return company
    
    async def create_company(self, company: CompanyCreateModel, session: AsyncSession) -> Company:
        company.name = company.name.capitalize()
        if company.description is not None:
            company.description = company.description.capitalize()
        company.uid = uuid.uuid4()
        await session.add(company)
        await session.commit()
        await session.refresh(company)
        return company
    
    async def delete_company(self, id: uuid.UUID, session: AsyncSession) -> None:
        statement = select(Company).where(Company.uid == id)
        result = await session.exec(statement)
        company = result.first()
        company.is_deleted = True
        session.add(company)
        await session.commit()
        await session.refresh(company)
    
    async def edit_company(self, company: Company, company_data: dict, session: AsyncSession) -> Company:
        company.name = company_data.name.capitalize()
        company.description = company_data.description
        if company_data.description is not None:
            company.description = company_data.description.capitalize()
        session.add(company)
        await session.commit()
        await session.refresh(company)
        return company