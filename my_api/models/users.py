from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from my_api.models import Base

if TYPE_CHECKING:
    from my_api.models import Brand, Product, StockLot, StockMovement


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now()
    )

    brands: Mapped[List['Brand']] = relationship(
        back_populates='user'
    )

    products: Mapped[List['Product']] = relationship(
        back_populates='user'
    )

    stock_lots: Mapped[List['StockLot']] = relationship(
        back_populates='user'
    )

    stock_movements: Mapped[List['StockMovement']] = relationship(
        back_populates='user'
    )
