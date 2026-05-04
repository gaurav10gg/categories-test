import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.banner_model import Banner
from app.models.category_model import Category
from app.models.product_model import Product
from app.schemas.catalog_schema import BannerResponse, HomePageResponse, ProductSummaryResponse
from app.services.category_service import CategoryService


class CatalogService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.category_service = CategoryService(db)

    async def get_homepage(self, recently_viewed_ids: list[uuid.UUID] | None = None) -> HomePageResponse:
        banners = await self.get_promotional_banners()
        categories = await self.category_service.get_active_categories()
        featured_categories = await self.category_service.get_featured_categories()
        recently_viewed = await self.get_recently_viewed_products(recently_viewed_ids or [])

        return HomePageResponse(
            banners=banners,
            categories=categories,
            featured_categories=featured_categories,
            recently_viewed_products=recently_viewed,
        )

    async def get_recently_viewed_products(self, product_ids: list[uuid.UUID]) -> list[ProductSummaryResponse]:
        if not product_ids:
            return []

        result = await self.db.execute(
            select(Product).where(
                Product.id.in_(product_ids),
            )
        )
        products = {product.id: product for product in result.scalars().all()}

        # Keep response order same as input list.
        ordered = [products[pid] for pid in product_ids if pid in products]
        return [
            ProductSummaryResponse(
                id=product.id,
                name=product.name,
                image_url=product.image_url,
                base_price=product.base_price,
                currency=product.currency,
                sku=product.sku,
                color=product.color,
                status=product.status,
                category_id=product.category_id,
            )
            for product in ordered
        ]

    async def get_promotional_banners(self, limit: int = 10) -> list[BannerResponse]:
        result = await self.db.execute(
            select(Banner)
            .where(Banner.is_active.is_(True))
            .order_by(Banner.sort_order.asc(), Banner.created_at.desc())
            .limit(limit)
        )
        banners = result.scalars().all()
        return [
            BannerResponse(
                banner_id=banner.banner_id,
                title=banner.title,
                image_url=banner.image_url,
                redirect_url=banner.redirect_url,
                sort_order=banner.sort_order,
            )
            for banner in banners
        ]

    async def validate_category_for_product(self, category_id: uuid.UUID) -> None:
        await self.category_service.validate_category_exists(category_id, require_active=True)
