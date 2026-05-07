from sqlalchemy.orm import Session
from typing import Optional

from app.products import models


async def verify_category_exist(category_id, db_session: Session) -> Optional[models.Category]:
    """
    Проверяет существование категории по её ID.

    :param category_id: Идентификатор категории.
    :param db_session: Сессия SQLAlchemy.
    :return: Объект Category, если найден, иначе None.
    """
    category_info = db_session.query(models.Category).filter(models.Category.id == category_id).first()
    return category_info

async def verify_product_exist(product_id: int, db_session: Session) -> Optional[models.Product]:
    """Проверяет существование товара по ID.
    :param product_id: Идентификатор продукта.
    :param db_session: Сессия SQLAlchemy.
    :return: Объект Product, если найден, иначе None.
    """
    return db_session.query(models.Product).filter(models.Product.id == product_id).first()