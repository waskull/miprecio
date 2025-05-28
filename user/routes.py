from typing import List
import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..config import Config

from ..auth.utils import create_url_safe_token

from ..auth.dependencies import RoleChecker, get_current_user

from ..utils.uuid_validator import is_valid_uuid

from ..errors import InsufficientPermission, InvalidUUID, UserAlreadyExists, UserNotFound, UserPasswordNotMatch

from .service import UserService
from .schemas import Role, UserCreateModel, UserEditModel, UserModel, UserPasswordEditModel
from ..db import get_session

user_service = UserService()
user_router = APIRouter()
role_checker = RoleChecker(["admin", "socio", "user"])
admin_checker = RoleChecker(["admin"])

@user_router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserModel])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_all_users(session)
    return users

@user_router.get("/top", status_code=status.HTTP_200_OK, response_model=List[UserModel])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_top_users(session)
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
    current_user = Depends(get_current_user),
    role: bool = Depends(role_checker),
    session: AsyncSession = Depends(get_session)):

    if not is_valid_uuid(id):
        raise InvalidUUID()
    user = await user_service.get_user_by_id(id=uuid.UUID(id, version=4), session=session)
    if user is None:
        raise UserNotFound()
    
    if user.uid is not current_user.uid and current_user.role is not Role.admin.value:
        raise InsufficientPermission()

    edited_user = await user_service.edit_user(user=user, user_data=user_data, session=session)
    return {"message": "Usuario editado"}

@user_router.patch("/password/{id}", status_code=status.HTTP_200_OK, )
async def update_password(
    id:str, 
    user_data: UserPasswordEditModel, 
    _: bool = Depends(role_checker),
    current_user = Depends(get_current_user),
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
    if user.uid is not current_user.uid and current_user.role is not Role.admin.value:
        raise InsufficientPermission()
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
    await user_service.delete_user(id=uuid.UUID(id, version=4), session=session)
    return {"message": "Usuario borrado"}

@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_partner_account(
    user_data: UserCreateModel,
    bg_tasks: BackgroundTasks,
    _: bool = Depends(admin_checker),
    session: AsyncSession = Depends(get_session),
):
    """
    Crea una cuenta de socio utilizando un correo un usuario, un nombre y un apellido
    params:
        user_data: UserCreateModel
    """
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()
    new_user = await user_service.create_user(user_data, session, is_partner=True)

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html = f"""
    <h1>Verify your Email</h1>
    <p>Por favor haz click aqui <a href="{link}">link</a> para verificar tu correo.</p>
    """

    emails = [email]

    subject = "Verifica tu correo"

    #send_email.delay(emails, subject, html)

    return {
        "message": "Cuenta creada, verifica tu correo para activar tu cuenta"
    }
