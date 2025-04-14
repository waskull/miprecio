from typing import List
import uuid
from fastapi import APIRouter, Depends, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..user.schemas import Role

from .schemas import CompanyModel, CompanyCreateModel

from ..auth.dependencies import RoleChecker, get_current_user

from ..utils.uuid_validator import is_valid_uuid

from ..errors import CompanyAlreadyExists, CompanyNotFound, InvalidUUID

from .service import CompanyService
from ..db import get_session

company_service = CompanyService()
company_router = APIRouter()
role_checker = RoleChecker([Role.admin.value, Role.partner.value, Role.user.value])

@company_router.get("/", status_code=status.HTTP_200_OK, response_model=List[CompanyModel])
async def get_all_companies(session: AsyncSession = Depends(get_session)):
    company = await company_service.get_all_companies(session)
    return company

@company_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CompanyModel)
async def get_company(id:str, session: AsyncSession = Depends(get_session)):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    company = await company_service.get_company_by_id(id=uuid.UUID(id, version=4), session=session)
    if company is None:
        raise CompanyNotFound()
    return company
@company_router.get("/company/{name}", status_code=status.HTTP_200_OK, response_model=CompanyModel)
async def get_company_by_name(name:str, session: AsyncSession = Depends(get_session)):
    company = await company_service.get_company_by_name(name=name.capitalize(), session=session)
    if company is None:
        raise CompanyNotFound()
    return company

@company_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(company: CompanyModel, session: AsyncSession = Depends(get_session), _: bool = Depends(role_checker),):
    category_exists = await company_service.get_company_by_name(name=company.name, session=session)
    if category_exists is not None:
        raise CompanyAlreadyExists()
    new_category = await company_service.create_company(company=company, session=session)
    return {"message": "Compañia creada"}
@company_router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_company(id:str, company_data: CompanyModel,_: bool = Depends(role_checker), session: AsyncSession = Depends(get_session), role_checker: bool = Depends(role_checker),):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    company = await company_service.get_category_by_id(id=uuid.UUID(id, version=4), session=session)
    if company is None:
        raise CompanyNotFound()
    category_exists = await company_service.get_category_by_name(name=company_data.name, session=session)
    if category_exists is not None and category_exists.uid != company.uid:
        raise CompanyAlreadyExists()
    edited_category = await company_service.edit_company(company=company, company_data=company_data, session=session)
    return {"message": "Compañia editada"}

@company_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_company(
    id:str, 
    _: bool = Depends(role_checker),
    session: AsyncSession = Depends(get_session)):    
    if not is_valid_uuid(id):
        raise InvalidUUID()
    company = await company_service.get_company_by_id(id=uuid.UUID(id, version=4), session=session)
    if company is None:
        raise CompanyNotFound()    
    await company_service.delete_company(id=uuid.UUID(id, version=4), session=session)
    return {"message": "Compañia borrada"}