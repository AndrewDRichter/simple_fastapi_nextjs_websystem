from datetime import datetime, date

from typing import List, TYPE_CHECKING

from sqlalchemy import func, String, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from my_api.models import Base

if TYPE_CHECKING:
    from my_api.models import User, Product, StockMovement


class StockLot(Base):
    __tablename__ = 'stock_lots'
    __table_args__ = (
        UniqueConstraint('code', 'product_id', name='uq_product_lot'),
        CheckConstraint('quantity >= 0', name='ck_lot_nonnegative'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    expires_at: Mapped[date | None] = mapped_column(nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False, default=0)

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now()
    )

    product: Mapped['Product'] = relationship(
        'Product',
        back_populates='stock_lots'
    )
    user: Mapped['User'] = relationship(
        'User',
        back_populates='stock_lots'
    )

    stock_movements: Mapped[List['StockMovement']] = relationship(
        back_populates='stock_lot'
    )
