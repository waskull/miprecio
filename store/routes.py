from typing import List
import uuid
from fastapi import APIRouter, Depends, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..user.schemas import Role

from .schemas import StoreCompanyModel, StoreCreateModel, StoreDeleteModel
from ..company.schemas import CompanyStoreModel

from ..auth.dependencies import RoleChecker, get_current_user

from ..utils.uuid_validator import is_valid_uuid

from ..errors import InvalidUUID, StoreAlreadyExists, StoreNotFound

from .service import StoreService
from ..db import get_session

store_service = StoreService()
store_router = APIRouter()
role_checker = RoleChecker([Role.admin.value, Role.partner.value, Role.user.value])

@store_router.get("/", status_code=status.HTTP_200_OK, response_model=list[CompanyStoreModel])
async def get_all_stores(session: AsyncSession = Depends(get_session)):
    store = await store_service.get_all_stores(session)
    return store
@store_router.get("/top", status_code=status.HTTP_200_OK, response_model=list[CompanyStoreModel])
async def get_all_stores(session: AsyncSession = Depends(get_session)):
    store = await store_service.get_top_stores(session)
    return store

@store_router.get("/stores", status_code=status.HTTP_200_OK, response_model=list[StoreCompanyModel])
async def get_all_stores(session: AsyncSession = Depends(get_session)):
    store = await store_service.get_stores(session)
    return store

@store_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CompanyStoreModel)
async def get_store(id:str, session: AsyncSession = Depends(get_session)):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    store = await store_service.get_store_by_id(id=uuid.UUID(id, version=4), session=session)
    if store is None:
        raise StoreNotFound()
    return store

@store_router.get("/company/{id}", status_code=status.HTTP_200_OK, response_model=CompanyStoreModel)
async def get_store_by_company(id:str, session: AsyncSession = Depends(get_session)):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    store = await store_service.get_store_by_company_id(id=uuid.UUID(id, version=4), session=session)
    if store is None:
        raise StoreNotFound()
    return store
@store_router.get("/company/{id}/product/{product_uid}", status_code=status.HTTP_200_OK, response_model=StoreCompanyModel)
async def get_store_by_company_store(id:str, product_uid:str, session: AsyncSession = Depends(get_session)):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    store = await store_service.get_store_by_company_product_uid(id=uuid.UUID(id, version=4), product_uid=uuid.UUID(product_uid, version=4), session=session)
    if store is None:
        raise StoreNotFound()
    return store

@store_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_store(
    store: StoreCreateModel, 
    session: AsyncSession = Depends(get_session),
    user_data=Depends(get_current_user),
    _: bool = Depends(role_checker),
    ):
    store_exists = await store_service.check_store(company_uid=store.company_uid, product_uid=store.product_uid, session=session)  
    if store_exists is not None:
        if store_exists.is_deleted is True:
            await store_service.enable_store(store=store_exists, session=session)
            return {"message": "El producto ha sido rehabilitado con exito"}
        else: raise StoreAlreadyExists()
    else:
        new_store = await store_service.create_store(store=store, user_data_id=user_data.uid, session=session)
        return {"message": "El producto ha sido creado con exito"}
@store_router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_store(id:str, company_data: StoreCreateModel,_: bool = Depends(role_checker), session: AsyncSession = Depends(get_session), role_checker: bool = Depends(role_checker),):
    print("ASDASDASDSAD: ", company_data)
    if not is_valid_uuid(id):
        raise InvalidUUID()
    store = await store_service.get_store_by_company_product_uid(id=uuid.UUID(id, version=4), product_uid=company_data.product_uid, session=session)
    if store is None:
        raise StoreNotFound()
    #store_exists = store_service.check_store(id=store.uid, product_uid=store.product_uid, session=session)
    #if store_exists is not None and store_exists.uid != store.uid:
    #    raise StoreAlreadyExists()
    edited_store = await store_service.edit_store(store=store, store_data=company_data, session=session)
    return {"message": "El producto ha sido editado con exito"}

@store_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_store(
    id:str, 
    company_data: StoreDeleteModel,
    _: bool = Depends(role_checker),
    session: AsyncSession = Depends(get_session)):    
    if not is_valid_uuid(id):
        raise InvalidUUID()
    print("antes de borrar: ", company_data)
    store = await store_service.get_store_by_company_product_uid(id=uuid.UUID(id, version=4), product_uid=company_data.product_uid, session=session)
    if store is None:
        raise StoreNotFound()    
    await store_service.delete_store(store=store, session=session)
    return {"message": "El producto ha sido borrado de la tienda con exito"}