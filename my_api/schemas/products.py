from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from my_api.schemas.users import UserPublicShortSchema
from my_api.schemas.brands import BrandPublicShortSchema


class ProductSchema(BaseModel):
    name: str
    brand_id: int


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None


class ProductPublicSchema(BaseModel):
    id: int
    name: str
    user: UserPublicShortSchema
    brand: BrandPublicShortSchema
    created_at: datetime
    updated_at: datetime


class ProductPublicShortSchema(BaseModel):
    id: int
    name: str
    brand: BrandPublicShortSchema


class ProductListPublicSchema(BaseModel):
    products: List[ProductPublicSchema]
