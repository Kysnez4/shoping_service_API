from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.cart import shema
from app.products.models import Product
from app.user import validator
from app.user.models import User
from app.cart.models import Cart, CartItems


async def add_items(cart_id: int, product_id: int, database: Session) -> None:
    cart_item = CartItems(cart_id=cart_id, product_id=product_id)
    database.add(cart_item)
    database.commit()
    database.refresh(cart_item)


async def add_product_to_cart(product_id: int, current_user: User, database: Session) -> dict:
    product = database.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found!")
    if product.quantity < 1:
        raise HTTPException(status_code=400, detail="Item out of stock!")

    user = await validator.verify_email_exist(email=current_user.email, db=database)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    cart = database.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        database.add(cart)
        database.commit()
        database.refresh(cart)

    await add_items(cart.id, product.id, database)
    return {"status": "Item added to cart!"}


async def add_multiple_products_to_cart(
    items: List[int], current_user: User, database: Session
) -> dict:
    user = await validator.verify_email_exist(email=current_user.email, db=database)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    cart = database.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        database.add(cart)
        database.commit()
        database.refresh(cart)

    added = []
    not_found = []
    out_of_stock = []

    for product_id in items:
        product = database.get(Product, product_id)
        if not product:
            not_found.append(product_id)
            continue
        if product.quantity < 1:
            out_of_stock.append(product_id)
            continue
        await add_items(cart.id, product_id, database)
        added.append(product_id)

    return {
        "status": "Items processed",
        "added": added,
        "not_found": not_found,
        "out_of_stock": out_of_stock
    }


async def get_all_items(current_user: User, database: Session) -> shema.ShowCart:
    user = await validator.verify_email_exist(email=current_user.email, db=database)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    cart = database.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        return shema.ShowCart(id=0, cart_items=[], total_price=0.0)

    # Подсчёт стоимости
    total = 0.0
    items_schema = []
    for item in cart.cart_items:
        if item.products:
            total += item.products.price
        items_schema.append(
            shema.ShowCartItems(
                id=item.id,
                products=item.products,
                created_date=item.created_date
            )
        )

    return shema.ShowCart(
        id=cart.id,
        cart_items=items_schema,
        total_price=total
    )


async def remove_cart_item(cart_item_id: int, current_user: User, database: Session) -> None:
    user = await validator.verify_email_exist(email=current_user.email, db=database)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    cart = database.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found!")

    item = database.query(CartItems).filter(
        CartItems.id == cart_item_id,
        CartItems.cart_id == cart.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found!")

    database.delete(item)
    database.commit()


async def clear_cart(current_user: User, database: Session) -> None:
    user = await validator.verify_email_exist(email=current_user.email, db=database)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    cart = database.query(Cart).filter(Cart.user_id == user.id).first()
    if cart:
        database.query(CartItems).filter(CartItems.cart_id == cart.id).delete()
        database.commit()


async def get_cart_total_price(current_user: User, database: Session) -> float:
    user = await validator.verify_email_exist(email=current_user.email, db=database)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    cart = database.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        return 0.0

    total = 0.0
    for item in cart.cart_items:
        if item.products:
            total += item.products.price
    return total