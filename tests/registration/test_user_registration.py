import pytest
import random
import string
from faker import Faker

fake = Faker()


def generate_valid_password():
    """Генерирует пароль, соответствующий требованиям приложения."""
    special_chars = "$%&!:"
    password_chars = [
        random.choice(string.ascii_uppercase),  # Заглавная буква
        random.choice(string.ascii_lowercase),  # Строчная буква
        random.choice(string.digits),  # Цифра
        random.choice(special_chars),  # Спецсимвол
    ]
    remaining_length = random.randint(4, 8)
    for _ in range(remaining_length):
        char_type = random.choice(["upper", "lower", "digit", "special"])
        if char_type == "upper":
            password_chars.append(random.choice(string.ascii_uppercase))
        elif char_type == "lower":
            password_chars.append(random.choice(string.ascii_lowercase))
        elif char_type == "digit":
            password_chars.append(random.choice(string.digits))
        else:
            password_chars.append(random.choice(special_chars))
    random.shuffle(password_chars)
    return "".join(password_chars)


@pytest.fixture
def valid_user_data():
    """Фикстура с валидными данными пользователя."""
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": f"+7{random.randint(1000000000, 9999999999)}",
        "password": generate_valid_password(),
    }