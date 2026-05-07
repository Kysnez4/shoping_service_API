from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

from app.user import hashing


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(
        Integer, ForeignKey("roles.id"), nullable=False, default=2
    )

    cart = relationship("Cart", back_populates="user_cart")
    order = relationship("Order", back_populates="user_info")
    role = relationship("Role", back_populates="users")

    def __init__(self, name, email, phone, password, role_id=2, *args, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.email = email
        self.phone = phone
        self.password = hashing.get_password_hash(password)
        self.role_id = role_id

    def check_password(self, password):
        return hashing.verify_password(self.password, password)

    @property
    def is_admin(self):
        return self.role_id == 1
