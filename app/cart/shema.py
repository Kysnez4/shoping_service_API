from typing import List
from pydantic import BaseModel, ConfigDict
import datetime

from app.products.shema import Product


class ShowCartItems(BaseModel):
    id: int
    products: Product
    created_date: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class ShowCart(BaseModel):
    id: int
    cart_items: List[ShowCartItems] = []
    total_price: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class AddMultipleItemsRequest(BaseModel):
    items: List[int]