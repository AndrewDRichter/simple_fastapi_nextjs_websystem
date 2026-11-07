from datetime import datetime

from typing import TYPE_CHECKING, Optional

from sqlalchemy import func, Integer, String, ForeignKey, Text, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from my_api.models import Base, User, StockLot


class StockMovement(Base):
    __tablename__ = 'stock_movements'
    __table_args__ = (
        CheckConstraint(
            'quantity_delta != 0',
            name='ck_movement_nonzero',
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity_delta: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str]
    notes: Mapped[Optional[str]] = mapped_column(Text, default=None)

    lot_id: Mapped[int] = mapped_column(ForeignKey('stock_lots.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    # updated_at: Mapped[datetime] = mapped_column(
    #     onupdate=func.now(), server_default=func.now()
    # )

    stock_lot: Mapped['StockLot'] = relationship(
        'StockLot',
        back_populates='stock_movements'
    )
    user: Mapped['User'] = relationship(
        'User',
        back_populates='stock_movements'
    )

    @validates('quantity_delta')
    def validate_quantity_delta(cls, k, v):
        if v == 0:
            raise ValueError('Movement quantity cannot be zero')
        return v
