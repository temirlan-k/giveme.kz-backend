import uuid
from enum import Enum
from app.config.db import Base
from sqlalchemy import Column, DateTime, String, ForeignKey, Enum as EnumType, UUID,Integer, func
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    items = relationship("Item", back_populates="category")

class Item(Base):
    __tablename__ = 'items'

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    image = Column(String(255))
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))  
    created_at_time = Column(DateTime, default=func.now())
    user = relationship("User",back_populates='items')
    category = relationship("Category", back_populates="items")
    orders = relationship("Order", back_populates="item")  
