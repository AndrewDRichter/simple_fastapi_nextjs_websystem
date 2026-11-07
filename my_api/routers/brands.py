from typing import Optional
from fastapi import APIRouter, status, Depends, HTTPException, Query

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from my_api.core.database import get_session
from my_api.core.security import get_current_user
from my_api.models import User, Brand
from my_api.schemas.brands import (
    BrandSchema,
    BrandPublicSchema,
    BrandUpdateSchema,
    BrandListPublicSchema,
)

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=BrandPublicSchema,
    summary='Create brand',
)
async def create_brand(
    brand: BrandSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):

    brand_exists = await db.scalar(
        select(exists().where(
            (Brand.name == brand.name) &
            (Brand.user_id == current_user.id))
        )
    )

    if brand_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Brand already exists',
        )

    db_brand = Brand(
        name=brand.name,
        user_id=current_user.id
    )

    db.add(db_brand)
    await db.commit()
    await db.refresh(db_brand)

    return db_brand

@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=BrandListPublicSchema,
    summary='List brands',
)
async def list_brands(
    offset: int = Query(0, ge=0, description='Records to jump'),
    limit: int = Query(100, ge=1, le=100, description='Number of records'),
    search: Optional[str] = Query(None, description='Search by name'),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    query = select(Brand).where(Brand.user_id == current_user.id)

    if search:
        search_filter = f'%{search}%'
        query = query.where(Brand.name.ilike(search_filter))

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    brands = result.scalars().all()

    return {
        'brands': brands,
        'offset': offset,
        'limit': limit,
    }

@router.get(
    path='/{brand_id}',
    status_code=status.HTTP_200_OK,
    response_model=BrandPublicSchema,
    summary='Brand details',
)
async def detail_brand(
    brand_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    brand = await db.scalar(
        select(Brand).where(
            (Brand.id == brand_id) &
            (Brand.user_id == current_user.id)
        )
    )

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Brand does not exist'
        )

    return brand

@router.put(
    path='/{brand_id}',
    status_code=status.HTTP_200_OK,
    response_model=BrandPublicSchema,
    summary='Update brand',
)
async def update_brand(
    brand_id: int,
    brand_update: BrandUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    brand = await db.scalar(
        select(Brand).where(
            (Brand.id == brand_id) &
            (Brand.user_id == current_user.id)
        )
    )

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='Brand not found',
        )

    update_data = brand_update.model_dump(exclude_unset=True)

    if 'name' in update_data and update_data['name'] != brand.name:
        name_exists = await db.scalar(
            select(exists().where(
                (Brand.name == update_data['name']) &
                (Brand.user_id == current_user.id)
            ))
        )

        if name_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Brand with this name already exists'
            )

    for field, value in update_data.items():
        setattr(brand, field, value)

    await db.commit()
    await db.refresh(brand)

    return brand

@router.delete(
    path='/{brand_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete brand'
)
async def delete_brand(
    brand_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    brand = await db.scalar(
        select(Brand)
        .options(selectinload(Brand.products))
        .where(
            (Brand.id == brand_id) &
            (Brand.user_id == current_user.id)
        )
    )

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Brand not found'
        )

    if len(brand.products) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Brand with products associated cannot be deleted',
        )

    await db.delete(brand)
    await db.commit()

    return
