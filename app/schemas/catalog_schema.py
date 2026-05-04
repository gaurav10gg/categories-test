import uuid

from pydantic import BaseModel

from app.schemas.category_schema import CategoryResponse


class BannerResponse(BaseModel):
    banner_id: uuid.UUID
    title: str
    image_url: str
    redirect_url: str | None
    sort_order: int


class ProductSummaryResponse(BaseModel):
    id: uuid.UUID
    category_id: uuid.UUID | None
    name: str | None


class HomePageResponse(BaseModel):
    banners: list[BannerResponse]
    categories: list[CategoryResponse]
    featured_categories: list[CategoryResponse]
    recently_viewed_products: list[ProductSummaryResponse]
