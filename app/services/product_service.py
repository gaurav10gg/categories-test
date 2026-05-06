import uuid
from typing import Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_model import Product
from app.schemas.catalog_schema import ProductSummaryResponse


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_products(
        self,
        category_id: uuid.UUID | None = None,
        subcategory_id: uuid.UUID | None = None,
        sort_by: Literal["price_asc", "price_desc", "newest"] = "newest",
        limit: int = 20,
        offset: int = 0,
    ) -> list[ProductSummaryResponse]:
        query = select(Product).where(Product.status == "active")

        if category_id is not None:
            query = query.where(Product.category_id == category_id)
        if subcategory_id is not None:
            query = query.where(Product.subcategory_id == subcategory_id)

        if sort_by == "price_asc":
            query = query.order_by(Product.base_price.asc(), Product.created_at.desc())
        elif sort_by == "price_desc":
            query = query.order_by(Product.base_price.desc(), Product.created_at.desc())
        else:
            query = query.order_by(Product.created_at.desc())

        query = query.limit(limit).offset(offset)
        result = await self.db.execute(query)
        products = result.scalars().all()

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
                subcategory_id=product.subcategory_id,
            )
            for product in products
        ]
