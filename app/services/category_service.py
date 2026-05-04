import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category_model import Category
from app.schemas.category_schema import CategoryCreateRequest, CategoryUpdateRequest


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_category(self, payload: CategoryCreateRequest) -> Category:
        category = Category(
            name=payload.name.strip(),
            image_url=payload.image_url,
            is_active=payload.is_active,
            is_featured=payload.is_featured,
            sort_order=payload.sort_order,
        )
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update_category(self, category_id: uuid.UUID, payload: CategoryUpdateRequest) -> Category:
        category = await self._get_category(category_id)
        if payload.name is not None:
            category.name = payload.name.strip()
        if payload.image_url is not None:
            category.image_url = payload.image_url
        if payload.is_featured is not None:
            category.is_featured = payload.is_featured

        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update_status(self, category_id: uuid.UUID, is_active: bool) -> Category:
        category = await self._get_category(category_id)
        category.is_active = is_active
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update_sort_order(self, category_id: uuid.UUID, sort_order: int) -> Category:
        category = await self._get_category(category_id)
        category.sort_order = sort_order
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def get_active_categories(self) -> list[Category]:
        result = await self.db.execute(
            select(Category)
            .where(
                Category.is_active.is_(True),
            )
            .order_by(Category.sort_order.asc(), Category.name.asc())
        )
        return list(result.scalars().all())

    async def get_featured_categories(self) -> list[Category]:
        result = await self.db.execute(
            select(Category)
            .where(
                Category.is_active.is_(True),
                Category.is_featured.is_(True),
            )
            .order_by(Category.sort_order.asc(), Category.name.asc())
        )
        return list(result.scalars().all())

    async def validate_category_exists(self, category_id: uuid.UUID, require_active: bool = True) -> Category:
        category = await self._get_category(category_id)
        if require_active and not category.is_active:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Category is inactive.",
            )
        return category

    async def _get_category(self, category_id: uuid.UUID) -> Category:
        result = await self.db.execute(
            select(Category).where(
                Category.category_id == category_id,
            )
        )
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )
        return category
