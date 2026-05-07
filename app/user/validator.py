from sqlalchemy.orm import Session
from typing import Optional
from pydantic import EmailStr

from app.user.models import User


async def verify_email_exist(email: EmailStr, db: Session) -> Optional[User]:
    """
    Проверяет, существует ли пользователь с указанным email.

    :param email: Email пользователя.
    :param db: Сессия SQLAlchemy.
    :return: Объект User, если найден, иначе None.
    """
    return db.query(User).filter(User.email == email).first()

async def verify_phone_exist(phone: str, db: Session) -> Optional[User]:
    """Проверяет, существует ли пользователь с таким номером телефона.
    :param phone: Phone пользователя.
    :param db: Сессия SQLAlchemy.
    :return: Объект User, если найден, иначе None.
    """
    return db.query(User).filter(User.phone == phone).first()
