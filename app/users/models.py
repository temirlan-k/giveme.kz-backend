import uuid
from enum import Enum
from app.config.db import Base
from sqlalchemy import Column, String, UUID, func, DateTime, Boolean,Enum as EnumType
from sqlalchemy.orm import relationship

class UserRole(Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'

class User(Base):
    __tablename__='users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=50), nullable=False)
    surname = Column(String(length=50), nullable=False)
    email = Column(String(length=320), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    is_active = Column(Boolean, default=False)
    is_needer = Column(Boolean, default=False)
    role = Column(EnumType(UserRole), default=UserRole.USER) # Corrected here

    items = relationship("Item", back_populates="user")
    orders = relationship("Order", back_populates="user")  
    def __str__(self):
        return f'#{self.id}:{self.name} {self.surname}'
