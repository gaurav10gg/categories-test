import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.catalog_schema import BannerResponse, HomePageResponse, ProductSummaryResponse
from app.services.catalog_service import CatalogService

router = APIRouter()


@router.get("/home", response_model=HomePageResponse)
async def get_homepage(
    recently_viewed_ids: list[uuid.UUID] | None = Query(default=None),
    db: AsyncSession = Depends(get_db_session),
) -> HomePageResponse:
    service = CatalogService(db)
    return await service.get_homepage(recently_viewed_ids=recently_viewed_ids)


@router.get("/trending-products", response_model=list[ProductSummaryResponse])
async def get_trending_products(
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_session),
) -> list[ProductSummaryResponse]:
    service = CatalogService(db)
    return await service.get_trending_products(limit)


@router.get("/recently-viewed-products", response_model=list[ProductSummaryResponse])
async def get_recently_viewed_products(
    product_ids: list[uuid.UUID] = Query(default=[]),
    db: AsyncSession = Depends(get_db_session),
) -> list[ProductSummaryResponse]:
    service = CatalogService(db)
    return await service.get_recently_viewed_products(product_ids)


@router.get("/promotional-banners", response_model=list[BannerResponse])
async def get_promotional_banners(
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db_session),
) -> list[BannerResponse]:
    service = CatalogService(db)
    return await service.get_promotional_banners(limit)
