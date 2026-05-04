from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.category_schema import CategoryDropdownItem, CategoryResponse
from app.services.category_service import CategoryService

router = APIRouter()


@router.get("", response_model=list[CategoryResponse])
async def get_active_categories(
    db: AsyncSession = Depends(get_db_session),
) -> list[CategoryResponse]:
    service = CategoryService(db)
    return await service.get_active_categories()


@router.get("/featured", response_model=list[CategoryResponse])
async def get_featured_categories(
    db: AsyncSession = Depends(get_db_session),
) -> list[CategoryResponse]:
    service = CategoryService(db)
    return await service.get_featured_categories()


@router.get("/dropdown", response_model=list[CategoryDropdownItem])
async def get_category_dropdown(
    db: AsyncSession = Depends(get_db_session),
) -> list[CategoryDropdownItem]:
    service = CategoryService(db)
    categories = await service.get_active_categories()
    return [CategoryDropdownItem(id=item.category_id, label=item.name) for item in categories]
