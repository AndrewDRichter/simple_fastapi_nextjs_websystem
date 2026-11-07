from typing import Optional
from fastapi import APIRouter, status, Depends, HTTPException, Query

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from my_api.core.database import get_session
from my_api.core.security import get_current_user
from my_api.models import User, Brand, Product
from my_api.schemas.products import (
    ProductSchema,
    ProductPublicSchema,
    ProductUpdateSchema,
    ProductListPublicSchema,
)

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=ProductPublicSchema,
    summary='Create product',
)
async def create_product(
    product: ProductSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    product_exists = await db.scalar(
        select(exists().where(
            (Product.name == product.name) &
            (Product.brand_id == product.brand_id) &
            (Product.user_id == current_user.id)
        ))
    )

    if product_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Product already exists',
        )

    brand_exists = await db.scalar(
        select(exists().where(
            (Brand.id == product.brand_id) &
            (Brand.user_id == current_user.id)
        ))
    )

    if not brand_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Brand not found',
        )

    db_product = Product(
        name=product.name,
        brand_id=product.brand_id,
        user_id=current_user.id
    )

    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)

    result = await db.execute(
        select(Product)
        .options(selectinload(Product.brand), selectinload(Product.user))
        .where(Product.id == db_product.id)
    )
    product_with_related = result.scalar_one()

    return product_with_related

@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=ProductListPublicSchema,
    summary='List products',
)
async def list_products(
    offset: int = Query(0, ge=0, description='Records to jump'),
    limit: int = Query(100, ge=1, le=100, description='Number of records'),
    search: Optional[str] = Query(None, description='Search by name'),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    query = select(Product).options(selectinload(Product.brand), selectinload(Product.user)).where(Product.user_id == current_user.id)

    if search:
        search_filter = f'%{search}%'
        query = query.where(Product.name.ilike(search_filter))

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    products = result.scalars().all()

    return {
        'products': products,
        'offset': offset,
        'limit': limit,
    }

@router.get(
    path='/{product_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProductPublicSchema,
    summary='Product Details',
)
async def detail_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    product = await db.scalar(
        select(Product)
        .options(selectinload(Product.brand), selectinload(Product.user))
        .where(
            (Product.id == product_id) &
            (Product.user_id == current_user.id)
        )
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Product not found',
        )

    return product

@router.put(
    path='/{product_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProductPublicSchema,
    summary='Update product',
)
async def update_product(
    product_id: int,
    product_update: ProductUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    product = await db.scalar(
        select(Product)
        .options(selectinload(Product.brand), selectinload(Product.user))
        .where(
            (Product.id == product_id) &
            (Product.user_id == current_user.id)
        )
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Product not found',
        )

    update_data = product_update.model_dump(exclude_unset=True)

    if 'name' in update_data and update_data['name'] != product.name:
        name_exists = await db.scalar(
            select(exists().where(
                (Product.name == update_data['name']) &
                (Product.brand_id == product.brand_id) &
                (Product.user_id == current_user.id)
            ))
        )

        if name_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Product already exists',
            )

    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return product

@router.delete(
    path='/{product_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete product',
)
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    product = await db.scalar(
        select(Product)
        .where(
            (Product.id == product_id) &
            (Product.user_id == current_user.id)
        )
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Product not found',
        )

    #TODO: Validar se produto não está associado a nenhum outro registro antes de deletar
    await db.delete(product)
    await db.commit()

    return
