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
    
    async def create_company(self, company: Company, user_data: dict, session: AsyncSession) -> Company:
        company_data_dict = company.model_dump()
        newcompany = Company(**company_data_dict)
        newcompany.name = newcompany.name.capitalize()
        if newcompany.description is not None:
            newcompany.description = newcompany.description.capitalize()
        newcompany.uid = uuid.uuid4()
        newcompany.user_uid = user_data.uid
        if newcompany.partner_uid is None: newcompany.partner_uid = newcompany.user_uid
        session.add(newcompany)
        await session.commit()
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