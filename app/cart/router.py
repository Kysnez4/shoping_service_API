from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import db
from app.user.shema import User
from . import services, shema
from app.auth import jwt

router = APIRouter(tags=["Cart"], prefix="/cart")


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(
    product_id: int,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(jwt.get_current_user)
):
    return await services.add_product_to_cart(product_id, current_user, database)


@router.post("/add-multiple", status_code=status.HTTP_201_CREATED)
async def add_multiple_products_to_cart(
    request: shema.AddMultipleItemsRequest,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(jwt.get_current_user)
):
    return await services.add_multiple_products_to_cart(request.items, current_user, database)


@router.get("/", response_model=shema.ShowCart)
async def get_all_cart_items(
    database: Session = Depends(db.get_db),
    current_user: User = Depends(jwt.get_current_user)
):
    return await services.get_all_items(current_user, database)


@router.get("/total-price", response_model=float)
async def get_cart_total_price(
    database: Session = Depends(db.get_db),
    current_user: User = Depends(jwt.get_current_user)
):
    return await services.get_cart_total_price(current_user, database)


@router.delete("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def remove_cart_item_by_id(
    cart_item_id: int,
    database: Session = Depends(db.get_db),
    current_user: User = Depends(jwt.get_current_user)
):
    await services.remove_cart_item(cart_item_id, current_user, database)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def clear_cart(
    database: Session = Depends(db.get_db),
    current_user: User = Depends(jwt.get_current_user)
):
    await services.clear_cart(current_user, database)
    return Response(status_code=status.HTTP_204_NO_CONTENT)