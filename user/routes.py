from typing import List
import uuid
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..utils.uuid_validator import is_valid_uuid

from ..errors import InvalidUUID, UserNotFound

from .service import UserService
from .schemas import UserCreateModel, UserModel
from ..db import get_session

user_service = UserService()
user_router = APIRouter()

@user_router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserModel])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_all_users(session)
    return users

@user_router.get("/{id}", response_model=UserModel, status_code=status.HTTP_200_OK, )
async def get_user(id:str, session: AsyncSession = Depends(get_session)):
    if not is_valid_uuid(id):
        raise InvalidUUID()
    user = await user_service.get_user_by_id(id=uuid.UUID(id, version=4), session=session)
    if user is None:
        raise UserNotFound()
    return user