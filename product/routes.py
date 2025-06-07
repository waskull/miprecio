from typing import List
import uuid
from fastapi import APIRouter, Depends, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..auth.dependencies import RoleChecker, get_current_user

from ..utils.uuid_validator import is_valid_uuid

from ..errors import InvalidUUID, ProductAlreadyExists, ProductNotFound

from ..user.service import UserService
from .service import ProductService
from .schemas import ProductCreateModel, ProductModel, ProductEditModel, ProductModelWithCategory
from ..db import get_session

user_service = UserService()
product_service = ProductService()
product_router = APIRouter()
role_checker = RoleChecker(["admin", "socio"])

@product_router.get("/", status_code=status.HTTP_200_OK, response_model=list[ProductModelWithCategory])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    product = await product_service.get_all_products(session)
    return product

@product_router.get("/top", status_code=status.HTTP_200_OK, response_model=list[ProductModelWithCategory])
async def get_top_users(session: AsyncSession = Depends(get_session)):
    product = await product_service.get_top_products(session)
    return product

@product_router.get("/{id}", response_model=ProductModel, status_code=status.HTTP_200_OK, )
async def get_product(id:str, session: AsyncSession = Depends(get_session)):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    user = await product_service.get_product_by_id(id=uuid.UUID(id, version=4), session=session)
    if user is None:
        raise ProductNotFound()
    return user

@product_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreateModel,
    session: AsyncSession = Depends(get_session),
    user_data=Depends(get_current_user), _: bool = Depends(role_checker),
):
    """
    Crea un producto utilizando un un nombre, un precio y una descripcion
    params:
        product_data: ProductCreateModel
    """
    
    product_exists = await product_service.product_exists(product_data.name, session)
    if product_exists:
        raise ProductAlreadyExists()
    
    product_data.user_uid = user_data.uid
    new_product = await product_service.create_product(product_data, session)
    return {
        "message": "Product creado",
        "data": new_product,
    }

@product_router.patch("/{id}", status_code=status.HTTP_200_OK, )
async def update_product(
    id:str, 
    product_data: ProductEditModel, 
    _: bool = Depends(role_checker),
    session: AsyncSession = Depends(get_session)):

    if not is_valid_uuid(id):
        raise InvalidUUID()
    product = await product_service.get_product_by_id(id=uuid.UUID(id, version=4), session=session)
    if product is None:
        raise ProductNotFound()
    edited_product = await product_service.edit_product(product=product, product_data=product_data, session=session)
    return {"message": "Producto editado"}

@product_router.delete("/{id}", status_code=status.HTTP_200_OK, )
async def delete_product(id:str,_: bool = Depends(role_checker), session: AsyncSession = Depends(get_session)):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    product = await product_service.get_product_by_id(id=uuid.UUID(id, version=4), session=session)
    if product is None:
        raise ProductNotFound()
    await product_service.delete_product(id=uuid.UUID(id, version=4), session=session)
    return {"message": "Producto borrado"}