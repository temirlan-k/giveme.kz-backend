import enum
import uuid
from app.config.db import Base

from sqlalchemy import (
    Column,
    DateTime,
    String,
    ForeignKey,
    Enum as EnumType,
    UUID,
    Integer,
    func,
)
from sqlalchemy.orm import relationship

class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    IN_DELIVERY="IN_DELIVERY"
    COMPLETED="COMPLETED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    contact_name = Column(String(length=50), nullable=False)
    address = Column(String(length=255), nullable=False)
    city = Column(String(length=100), nullable=False)
    phone_number = Column(String(length=20), nullable=False)
    status = Column(EnumType(OrderStatus),default=OrderStatus.PENDING)
    created_at_time = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="orders")
    item = relationship("Item", back_populates="orders")
