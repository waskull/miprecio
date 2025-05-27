from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from ..product.schemas import UserProductsModel
from ..user.schemas import UserCreateModel

from ..db import get_session

from .dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    RoleChecker,
    get_current_user,
)
from .schemas import (
    UserLoginModel,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel,
)
from ..user.service import UserService
from ..auth.service import AuthService
from .utils import (
    create_access_token,
    verify_password,
    generate_passwd_hash,
    create_url_safe_token,
    decode_url_safe_token,
)
from ..errors import UserAlreadyExists, UserNotFound, InvalidCredentials, InvalidToken
from ..config import Config
from ..db import get_session
#from ..celery_tasks import send_email

auth_router = APIRouter()
user_service = UserService()
auth_service = AuthService()
role_checker = RoleChecker(["admin", "user"])
only_admin_checker = RoleChecker(["admin"])


REFRESH_TOKEN_EXPIRY = 2


# Bearer Token


@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    emails = emails.addresses

    html = "<h1>Bienvenido a MiPrecio</h1>"
    subject = "Bienvenido"

    #send_email.delay(emails, subject, html)

    return {"message": "Correo enviado"}


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_Account(
    user_data: UserCreateModel,
    bg_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    """
    Crea una cuenta de usuario utilizando un correo un usuario, un nombre y un apellido
    params:
        user_data: UserCreateModel
    """
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()
    new_user = await user_service.create_user(user_data, session)

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
        "message": "Cuenta creada, verifica tu correo para activar tu cuenta",
        "user": new_user,
    }


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Cuenta verificada exitosamente"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Ocurrio un error durante la verificación"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_users(
    login_data: UserLoginModel,
    is_mobile: bool = False,
    session: AsyncSession = Depends(get_session),
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            #print("CLIENT: "+ request.user)
            response = JSONResponse(
                content={
                    "message": "Inicio de sesión exitoso"+str(is_mobile),
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email, 
                        "uid": str(user.uid),
                        "role": user.role,                    
                        "fullname": user.fullname
                    },
                }
            )
            response.set_cookie(key="access_token",secure=False, value=access_token, httponly=True, expires=3600*24*REFRESH_TOKEN_EXPIRY, samesite="lax")
            response.set_cookie(key="refresh_token",secure=False, value=refresh_token, httponly=True, expires=(3600*24*REFRESH_TOKEN_EXPIRY)*7, samesite="lax")
            return response

    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken


@auth_router.get("/me")
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    token = token_details["token"]

    await auth_service.add_token_to_blocklist(token, session)

    return JSONResponse(
        content={"message": "Sesión cerrada correctamente"}, status_code=status.HTTP_200_OK
    )



@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
    <h1>Reinicio de contraseña</h1>
    <p>Por favor haz click <a href="{link}">link</a> para reiniciar tu contraseña</p>
    """
    subject = "Reinicio de contraseña"

    #send_email.delay([email], subject, html_message)
    return JSONResponse(
        content={
            "message": "Por favor sigue las instrucciones del correo para actualizar tu contraseña",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    new_password = passwords.new_password
    confirm_password = passwords.confirm_new_password

    if new_password != confirm_password:
        raise HTTPException(
            detail="Las contraseñas no coinciden", status_code=status.HTTP_400_BAD_REQUEST
        )

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        passwd_hash = generate_passwd_hash(new_password)
        await user_service.update_user(user, {"password_hash": passwd_hash}, session)

        return JSONResponse(
            content={"message": "Contraseña reiniciada exitosamente"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Un error ha ocurrido durante el cambio de contraseña."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
