from pydantic import BaseModel, constr, ConfigDict
from typing import Optional
from datetime import datetime


class Category(BaseModel):
    name: constr(min_length=2, max_length=50)


class DisplayCategory(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    id: Optional[int]
    name: str
    quantity: int
    description: str
    price: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class Product(ProductBase):
    category_id: int


class DisplayProduct(ProductBase):
    category: DisplayCategory

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: constr(min_length=1, max_length=50)
    quantity: int
    description: str
    price: int
    category_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    price: Optional[int] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None