from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException, Query

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from my_api.core.database import get_session
from my_api.core.security import get_current_user
from my_api.models import User, Product, StockLot
from my_api.schemas.stock_lots import (
    StockLotPublicSchema,
    StockLotPublicShortSchema,
    StockLotListPublicSchema,
)

router = APIRouter()

@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=StockLotListPublicSchema,
    summary='List stock lots',
)
async def list_stock_lots(
    offset: int = Query(0, ge=0, description='Records to jump'),
    limit: int = Query(100, ge=1, le=100, description='Number of records'),
    search: Optional[str] = Query(None, description='Search by lot code'),
    product_id: Optional[int] = Query(None, description='Search by product id'),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    query = select(StockLot).options(selectinload(StockLot.product).selectinload(Product.brand), selectinload(StockLot.user)).where(StockLot.user_id == current_user.id)

    if search:
        search_filter = f'%{search}%'
        query = query.where(StockLot.code.ilike(search_filter))

    if product_id:
        query = query.where(StockLot.product_id == product_id)

    query = query.order_by(StockLot.id).offset(offset).limit(limit)

    result = await db.execute(query)
    stock_lots = result.scalars().all()

    return {
        'stock_lots': stock_lots,
        'offset': offset,
        'limit': limit,
    }
