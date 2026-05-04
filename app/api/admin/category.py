import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.category_schema import (
    CategoryCreateRequest,
    CategoryResponse,
    CategorySortOrderUpdateRequest,
    CategoryStatusUpdateRequest,
    CategoryUpdateRequest,
)
from app.services.category_service import CategoryService

router = APIRouter()


@router.post("", response_model=CategoryResponse)
async def create_category(
    payload: CategoryCreateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CategoryResponse:
    service = CategoryService(db)
    return await service.create_category(payload)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: uuid.UUID,
    payload: CategoryUpdateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CategoryResponse:
    service = CategoryService(db)
    return await service.update_category(category_id, payload)


@router.patch("/{category_id}/status", response_model=CategoryResponse)
async def update_category_status(
    category_id: uuid.UUID,
    payload: CategoryStatusUpdateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CategoryResponse:
    service = CategoryService(db)
    return await service.update_status(category_id, payload.is_active)


@router.patch("/{category_id}/sort-order", response_model=CategoryResponse)
async def update_category_sort_order(
    category_id: uuid.UUID,
    payload: CategorySortOrderUpdateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CategoryResponse:
    service = CategoryService(db)
    return await service.update_sort_order(category_id, payload.sort_order)
