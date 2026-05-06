import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    image_url: str | None = None
    is_active: bool = True
    is_featured: bool = False
    sort_order: int = 0


class CategoryUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    image_url: str | None = None
    is_featured: bool | None = None


class CategoryStatusUpdateRequest(BaseModel):
    is_active: bool


class CategorySortOrderUpdateRequest(BaseModel):
    sort_order: int


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: uuid.UUID
    name: str
    image_url: str | None
    is_active: bool
    is_featured: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime


class CategoryDropdownItem(BaseModel):
    id: uuid.UUID
    label: str


class SubcategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subcategory_id: uuid.UUID
    category_id: uuid.UUID
    name: str
    is_active: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime
