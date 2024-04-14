import uuid
from app.config.db import Base
from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey, UUID, Integer, func,Enum as EnumType
from sqlalchemy.orm import relationship

class ItemStatus(Enum):
    REVIEW='REVIEW'
    ACTIVE='ACTIVE'
    REMOVED='REMOVED'

    def __str__(self):
        return self.value

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    items = relationship("Item", back_populates="category")


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at_time = Column(DateTime, default=func.now())
    is_publish = Column(Boolean,default=False)
    status = Column(EnumType(ItemStatus),default=ItemStatus.REVIEW)
    contact_phone_number = Column(String(20)) 
    contact_address = Column(String(255))
    bonus = Column(Integer,default=0)  

    user = relationship("User", back_populates="items")
    category = relationship("Category", back_populates="items")
    orders = relationship("Order", back_populates="item")
