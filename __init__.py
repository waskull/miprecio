from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware
from .errors import register_all_errors
from .middleware import register_middleware
from .auth.routes import auth_router
from .user.routes import user_router
from .product.routes import product_router
from .category.routes import category_router
from .company.routes import company_router
from .store.routes import store_router
from .db import engine

version = "v1"

description = """
A REST API for a price product review web service.

This REST API is able to;
- Create Read Update And delete products
- Add reviews to products
- Add tags to Products e.t.c.
    """

version_prefix =f"/api/{version}"
SQLModel.metadata.create_all(engine)
app = FastAPI(
    title="MiPrecio",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Martin C",
        "url": "https://github.com/waskull",
        "email": "mrtncsto@gmail.com",
    },
    terms_of_service="httpS://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc"
)

@app.get("/health", tags=["root"], include_in_schema=False, response_model=dict)
async def read_root():
    return {"message": "Bv"}


register_all_errors(app)

register_middleware(app)
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
app.include_router(user_router, prefix=f"{version_prefix}/user", tags=["user"])
app.include_router(product_router, prefix=f"{version_prefix}/product", tags=["product"])
app.include_router(category_router, prefix=f"{version_prefix}/category", tags=["category"])
app.include_router(company_router, prefix=f"{version_prefix}/company", tags=["company"])
app.include_router(store_router, prefix=f"{version_prefix}/store", tags=["store"])