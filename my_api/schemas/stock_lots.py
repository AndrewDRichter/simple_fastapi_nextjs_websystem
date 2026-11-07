from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from my_api.schemas.users import UserPublicShortSchema
from my_api.schemas.products import ProductPublicShortSchema


class StockLotPublicSchema(BaseModel):
    id: int
    code: str
    expires_at: date
    quantity: int
    product: ProductPublicShortSchema
    user: UserPublicShortSchema


class StockLotPublicShortSchema(BaseModel):
    id: int
    code: str
    expires_at: date
    quantity: int
    product: ProductPublicShortSchema


class StockLotListPublicSchema(BaseModel):
    stock_lots: List[StockLotPublicSchema]
