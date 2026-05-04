from fastapi import FastAPI

from app.api.admin.category import router as admin_category_router
from app.api.public.catalog import router as public_catalog_router
from app.api.public.category import router as public_category_router


def create_app() -> FastAPI:
    app = FastAPI(title="Catalog Service", version="1.0.0")

    app.include_router(admin_category_router, prefix="/admin/categories", tags=["Admin Categories"])
    app.include_router(public_category_router, prefix="/categories", tags=["Public Categories"])
    app.include_router(public_catalog_router, prefix="/catalog", tags=["Catalog"])

    return app


app = create_app()
