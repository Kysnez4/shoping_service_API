from passlib.context import CryptContext

# Создание контекста для хеширования паролей с использованием argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли обычный пароль хешированному.

    :param plain_password: Пароль в обычном виде (введённый пользователем).
    :param hashed_password: Хеш пароля, сохранённый в базе данных.
    :return: True, если пароли совпадают, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Хеширует пароль для безопасного хранения.

    :param password: Пароль в обычном виде.
    :return: Хешированный пароль.
    """
    return pwd_context.hash(password)
