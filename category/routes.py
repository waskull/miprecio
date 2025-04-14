from typing import List
import uuid
from fastapi import APIRouter, Depends, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import CateModel, CategoryModel

from ..auth.dependencies import RoleChecker, get_current_user

from ..utils.uuid_validator import is_valid_uuid

from ..errors import CategoryAlreadyExists, CategoryNotFound, InvalidUUID

from .service import CategoryService
from ..db import get_session

category_service = CategoryService()
category_router = APIRouter()
role_checker = RoleChecker(["admin"])

@category_router.get("/", status_code=status.HTTP_200_OK, response_model=List[CateModel])
async def get_all_categories(session: AsyncSession = Depends(get_session)):
    category = await category_service.get_all_categories(session)
    return category

@category_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CateModel)
async def get_category(id:str, session: AsyncSession = Depends(get_session)):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    category = await category_service.get_category_by_id(id=uuid.UUID(id, version=4), session=session)
    if category is None:
        raise CategoryNotFound()
    return category
@category_router.get("/category/{name}", status_code=status.HTTP_200_OK, response_model=CateModel)
async def get_category_by_name(name:str, session: AsyncSession = Depends(get_session)):
    category = await category_service.get_category_by_name(name=name.capitalize(), session=session)
    if category is None:
        raise CategoryNotFound()
    return category

@category_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryModel, session: AsyncSession = Depends(get_session), _: bool = Depends(role_checker),):
    category_exists = await category_service.get_category_by_name(name=category.name, session=session)
    if category_exists is not None:
        raise CategoryAlreadyExists()
    new_category = await category_service.create_category(category=category, session=session)
    return {"message": "Categoria creada"}
@category_router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_category(id:str, category_data: CateModel,_: bool = Depends(role_checker), session: AsyncSession = Depends(get_session), role_checker: bool = Depends(role_checker),):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    category = await category_service.get_category_by_id(id=uuid.UUID(id, version=4), session=session)
    if category is None:
        raise CategoryNotFound()
    category_exists = await category_service.get_category_by_name(name=category_data.name, session=session)
    if category_exists is not None and category_exists.uid != category.uid:
        raise CategoryAlreadyExists()
    edited_category = await category_service.edit_category(category=category, category_data=category_data, session=session)
    return {"message": "Categoria editada"}

@category_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_category(
    id:str, 
    _: bool = Depends(role_checker),
    session: AsyncSession = Depends(get_session)):    
    if not is_valid_uuid(id):
        raise InvalidUUID()
    category = await category_service.get_category_by_id(id=uuid.UUID(id, version=4), session=session)
    if category is None:
        raise CategoryNotFound()    
    await category_service.delete_category(id=uuid.UUID(id, version=4), session=session)
    return {"message": "Categoria borrada"}