from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from my_api.schemas.users import UserPublicShortSchema


class BrandSchema(BaseModel):
    name: str


class BrandUpdateSchema(BaseModel):
    name: Optional[str] = None


class BrandPublicSchema(BaseModel):
    id: int
    name: str
    user: UserPublicShortSchema
    created_at: datetime
    updated_at: datetime


class BrandListPublicSchema(BaseModel):
    brands: List[BrandPublicSchema]


class BrandPublicShortSchema(BaseModel):
    id: int
    name: str
