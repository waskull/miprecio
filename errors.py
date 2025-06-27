from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError

class MyPrice(Exception):
    """Esta es una clase base para las excepciones personalizadas."""

    pass

class InvalidUUID(MyPrice):
    """El usuario ha proporcionado un uuid invalido."""

    pass

class InvalidToken(MyPrice):
    """El usuario ha proporcionado un token invalido."""

    pass


class RevokedToken(MyPrice):
    """El usuario ha proporcionado un token que ya fue revocado."""

    pass


class AccessTokenRequired(MyPrice):
    """El usuario ha proporcionado un refresh token cuando un access token es necesario."""

    pass


class RefreshTokenRequired(MyPrice):
    """El usuario ha proporcionado un refresh token cuando un access token es necesario."""

    pass


class UserAlreadyExists(MyPrice):
    """El usuario ya existe."""

    pass

class UserPasswordNotMatch(MyPrice):
    """La nueva clave y la confirmacion de la clave no coinciden."""
    pass

class UserPasswordMatch(MyPrice):
    """La nueva clave y la vieja clave son iguales."""
    pass

class InvalidCredentials(MyPrice):
    """El usuario ha proporcionado credenciales invalidas."""

    pass


class InsufficientPermission(MyPrice):
    """El usuario no tiene los permisos suficientes para realizar dicha acción."""

    pass


class ProductNotFound(MyPrice):
    """Producto no encontrado"""

    pass

class ProductAlreadyExists(MyPrice):
    """Producto ya existente"""

    pass


class CategoryNotFound(MyPrice):
    """Categoria no encontrada"""

    pass


class CategoryAlreadyExists(MyPrice):
    """Categoria ya existente"""

    pass

class CompanyNotFound(MyPrice):
    """Compañia no encontrada"""

    pass

class CompanyAlreadyExists(MyPrice):
    """Compañia ya existente"""

    pass

class StoreNotFound(MyPrice):
    """Tienda no encontrada"""

    pass

class StoreAlreadyExists(MyPrice):
    """Tienda ya existente"""

    pass


class UserNotFound(MyPrice):
    """Usuario no encontrado"""

    pass


class AccountNotVerified(Exception):
    """Cuentan no verificada"""
    pass

def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: MyPrice):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "El usuario ya existe",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Usuario no encontrado",
                "error_code": "user_not_found",
            },
        ),
    )

    app.add_exception_handler(
        UserPasswordNotMatch,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "La nueva contraseña y la contraseña de confirmacion no coinciden",
                "error_code": "password_not_match",
            },
        ),
    )

    app.add_exception_handler(
        UserPasswordMatch,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "La nueva contraseña y la vieja contraseña son iguales",
                "error_code": "password_match",
            },
        ),
    )

    app.add_exception_handler(
        ProductNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Producto no encontrado",
                "error_code": "book_not_found",
            },
        ),
    )
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Correo o contraseña invalida",
                "error_code": "invalid_email_or_password",
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "El token es invalido o ha expirado",
                "resolution": "Por favor obten un nuevo token",
                "error_code": "invalid_token",
            },
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "El token es invalido o ha sido revocado",
                "resolution": "Por favor obten un nuevo token",
                "error_code": "token_revoked",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Por favor provea un refresh token valido",
                "resolution": "Por favor provea un refresh token",
                "error_code": "access_token_required",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Por favor provea un refresh token valido",
                "resolution": "Por favor provea un refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "No tienes los permisos necesarios para realizar dicha acción",
                "error_code": "insufficient_permissions",
            },
        ),
    )
    app.add_exception_handler(
        CategoryNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Categoria no encontrada", "error_code": "category_not_found"},
        ),
    )

    app.add_exception_handler(
        CategoryAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Nombre de categoria ya existente",
                "error_code": "category_exists",
            },
        ),
    )

    app.add_exception_handler(
        StoreNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Tienda no encontrada", "error_code": "store_not_found"},
        ),
    )

    app.add_exception_handler(
        StoreAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Uno de los productos elegidos ya ha sido agregado previamente a la tienda",
                "error_code": "store_exists",
            },
        ),
    )

    app.add_exception_handler(
        CompanyNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Compañia no encontrada", "error_code": "company_not_found"},
        ),
    )

    app.add_exception_handler(
        CompanyAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Nombre de compañia ya existente",
                "error_code": "company_exists",
            },
        ),
    )

    app.add_exception_handler(
        ProductNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Producto no encontrado",
                "error_code": "product_no_encontrado",
            },
        ),
    )

    app.add_exception_handler(
        ProductAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Producto ya existente",
                "error_code": "product_exists",
            }
        )
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Cuenta no verificada",
                "error_code": "account_not_verified",
                "resolution":"Por favor verifique su correo para mas detalles"
            },
        ),
    )

    app.add_exception_handler(
        InvalidUUID,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "petición invalida",
                "error_code": "invalid_request",
            },
        )
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Algo salio mal",
                "error_code": "internal_server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Algo salio mal",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )