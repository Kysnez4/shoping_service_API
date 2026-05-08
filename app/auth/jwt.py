from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.auth import shema
from app import config
from app.user import models
from app import db

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict) -> str:
    """
    Создаёт JWT access token с заданными данными и временем жизни.

    :param data: Словарь с полезной нагрузкой (например, email пользователя).
    :return: Закодированный JWT token в виде строки.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> shema.TokenData:
    """
    Проверяет валидность JWT токена и извлекает email из полезной нагрузки.

    :param token: JWT токен в виде строки.
    :param credentials_exception: Исключение, которое вызывается при ошибке валидации.
    :raises credentials_exception: При ошибке декодирования или отсутствии email.
    :return: Объект TokenData
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = shema.TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme)) -> shema.TokenData:
    """
    Зависимость FastAPI, которая извлекает и проверяет текущего пользователя из переданного JWT токена.

    :param data: JWT токен из заголовка Authorization Bearer.
    :raises HTTPException: При недействительном или отсутствующем токене.
    :return: Данные токена (email пользователя).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(data, credentials_exception)


async def get_current_user_full(
    token_data: shema.TokenData = Depends(get_current_user),
    database: Session = Depends(db.get_db),
) -> models.User:
    """
    Зависимость FastAPI, которая возвращает полный объект пользователя из БД.
    """
    user = (
        database.query(models.User)
        .filter(models.User.email == token_data.email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_admin(user: models.User = Depends(get_current_user_full)) -> models.User:
    """
    Зависимость FastAPI, которая проверяет, является ли пользователь администратором.
    Возвращает пользователя только если он админ, иначе выбрасывает 403.
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin rights required"
        )
    return user
