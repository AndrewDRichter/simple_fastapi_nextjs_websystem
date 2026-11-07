from datetime import datetime

from typing import TYPE_CHECKING, List

from sqlalchemy import func, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from my_api.models import Base

if TYPE_CHECKING:
    from my_api.models import User, Product


class Brand(Base):
    __tablename__ = 'brands'
    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='uq_brand_user'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
    )

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), server_default=func.now()
    )

    user: Mapped['User'] = relationship(
        'User',
        back_populates='brands'
    )
    products: Mapped[List['Product']] = relationship(
        back_populates='brand'
    )
