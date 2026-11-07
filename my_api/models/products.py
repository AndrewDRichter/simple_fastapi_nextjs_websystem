from datetime import datetime

from typing import List, TYPE_CHECKING

from sqlalchemy import func, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from my_api.models import Base

if TYPE_CHECKING:
    from my_api.models import Brand, User, StockLot


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = (
        UniqueConstraint('name', 'brand_id', name='uq_brand_product'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    brand_id: Mapped[int] = mapped_column(ForeignKey('brands.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now()
    )

    brand: Mapped['Brand'] = relationship(
        'Brand',
        back_populates='products'
    )
    user: Mapped['User'] = relationship(
        'User',
        back_populates='products'
    )

    stock_lots: Mapped[List['StockLot']] = relationship(
        back_populates='product'
    )
