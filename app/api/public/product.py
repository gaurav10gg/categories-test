import uuid
from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.catalog_schema import ProductSummaryResponse
from app.services.product_service import ProductService

router = APIRouter()


@router.get("", response_model=list[ProductSummaryResponse])
async def list_products(
    category_id: uuid.UUID | None = Query(default=None),
    sort_by: Literal["price_asc", "price_desc", "newest"] = Query(default="newest"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db_session),
) -> list[ProductSummaryResponse]:
    service = ProductService(db)
    return await service.list_products(
        category_id=category_id,
        sort_by=sort_by,
        limit=limit,
        offset=offset,
    )
