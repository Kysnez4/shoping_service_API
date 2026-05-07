from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.user import models
from app.user import shema


async def new_user_register(request: shema.User, database: Session) -> models.User:
    """
    Создаёт нового пользователя на основе переданных данных.

    :param request: Объект с данными нового пользователя.
    :param database: Сессия базы данных.
    :return: Созданный пользователь (модель).
    """
    new_user = models.User(
        name=request.name,
        email=request.email,
        phone=request.phone,
        password=request.password,
        role_id=request.role_id if hasattr(request, "role_id") else 2,
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


async def all_users(database: Session) -> List[shema.DisplayUser]:
    """
    Возвращает список всех пользователей.
    """
    users = database.query(models.User).all()
    return [shema.DisplayUser.model_validate(user) for user in users]


async def get_user_by_id(user_id: int, database: Session) -> models.User:
    """
    Получает пользователя по ID.
    """
    user_info = database.query(models.User).get(user_id)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_info


async def delete_user_by_id(user_id: int, database: Session) -> None:
    """
    Удаляет пользователя по ID.
    """
    user = database.query(models.User).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    database.delete(user)
    database.commit()


async def update_user_role(
    user_id: int, role_id: int, database: Session
) -> models.User:
    """
    Обновляет роль пользователя.
    """
    user = await get_user_by_id(user_id, database)

    # Проверяем, существует ли роль
    role = database.query(models.Role).get(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    user.role_id = role_id
    database.commit()
    database.refresh(user)
    return user


async def get_users_by_role(role_id: int, database: Session) -> List[models.User]:
    """
    Получает всех пользователей с определенной ролью.
    """
    users = database.query(models.User).filter(models.User.role_id == role_id).all()
    return users


async def get_user_with_role(user_id: int, database: Session) -> Optional[models.User]:
    """
    Получает пользователя вместе с его ролью.
    """
    user = database.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
