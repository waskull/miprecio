from typing import List
import uuid
from fastapi import APIRouter, Depends, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..auth.dependencies import RoleChecker

from ..utils.uuid_validator import is_valid_uuid

from ..errors import InsufficientPermission, InvalidUUID, UserNotFound, UserPasswordNotMatch

from .service import UserService
from .schemas import Role, UserEditModel, UserModel, UserPasswordEditModel
from ..db import get_session

user_service = UserService()
user_router = APIRouter()
role_checker = RoleChecker(["admin", "socio", "user"])

@user_router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserModel])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_all_users(session)
    return users

@user_router.get("/{id}", response_model=UserModel, status_code=status.HTTP_200_OK)
async def get_user(id:str, session: AsyncSession = Depends(get_session)):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    user = await user_service.get_user_by_id(id=uuid.UUID(id, version=4), session=session)
    if user is None:
        raise UserNotFound()
    return user

@user_router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_user(
    id:str, 
    user_data: UserEditModel, 
    _: bool = Depends(role_checker),
    session: AsyncSession = Depends(get_session)):

    if not is_valid_uuid(id):
        raise InvalidUUID()
    user = await user_service.get_user_by_id(id=uuid.UUID(id, version=4), session=session)
    if user is None:
        raise UserNotFound()
    edited_user = await user_service.edit_user(user=user, user_data=user_data, session=session)
    return {"message": "Usuario editado"}

@user_router.patch("/password/{id}", status_code=status.HTTP_200_OK, )
async def update_password(
    id:str, 
    user_data: UserPasswordEditModel, 
    _: bool = Depends(role_checker),
    session: AsyncSession = Depends(get_session)):

    if user_data.newpassword != user_data.confirm_password:
        raise UserPasswordNotMatch()
    
    if user_data.old_password == user_data.newpassword:
        raise UserPasswordNotMatch()

    if not is_valid_uuid(id):
        raise InvalidUUID()
    user = await user_service.get_user_by_id(id=uuid.UUID(id, version=4), session=session)
    if user is None:
        raise UserNotFound()
    edited_user_password = await user_service.edit_user_password(user=user, formpassword=user_data.newpassword, session=session)
    return {"message": "Contraseña editada"}

@user_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_product(id:str,_: bool = Depends(role_checker), session: AsyncSession = Depends(get_session)):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    user = await user_service.get_user_by_id(id=uuid.UUID(id, version=4), session=session)
    if user is None:
        raise UserNotFound()
    if user.role == Role.admin.value:
        raise InsufficientPermission()
    await user_service.delete_user(id, session)
    return {"message": "Usuario borrado"}