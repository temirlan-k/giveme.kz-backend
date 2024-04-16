import uuid
from enum import Enum
from app.config.db import Base
from sqlalchemy import (
    Column,
    String,
    UUID,
    func,
    DateTime,
    Boolean,
    Enum as EnumType,
    ForeignKey,
    Integer
)
from sqlalchemy.orm import relationship
from app.orders.models import Order
from app.users.utils import generate_code


class UserRole(Enum):
    USER = "USER"
    ADMIN = "ADMIN"

    def __str__(self):
        return self.value

class DocumentStatus(Enum):
    NULL = 'NULL'
    ERROR = 'ERROR'
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
        
    def __str__(self):
        return self.value



class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=50), nullable=False)
    surname = Column(String(length=50), nullable=False)
    email = Column(String(length=320), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    is_active = Column(Boolean, default=False)
    is_needer = Column(Boolean, default=False)
    role = Column(EnumType(UserRole), default=UserRole.USER)

    bar_code = Column(Integer, default=generate_code, unique=True)

    items = relationship("Item", back_populates="user")
    orders = relationship("Order", back_populates="user")
    needer_files = relationship("UserNeederDocuments",back_populates='user')

    def __str__(self):
        return f"#{self.id}:{self.name} {self.surname}"


class UserNeederDocuments(Base):
    __tablename__ = 'needer_files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),ForeignKey('users.id'))
    electronic_id = Column(String(255),nullable=False)
    benefit_document = Column(String(255),nullable=False)
    user_photo = Column(String(255),nullable=False)
    is_verified = Column(Boolean,default=False)
    status = Column(EnumType(DocumentStatus),default=DocumentStatus.PENDING)

    user = relationship("User", back_populates="needer_files")

    def __str__(self):
        return f'{self.user_id} - {self.is_verified}'