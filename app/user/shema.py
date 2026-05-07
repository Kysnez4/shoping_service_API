from pydantic import BaseModel, constr, EmailStr, ConfigDict, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class Role(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


from pydantic import BaseModel, constr, EmailStr, ConfigDict, field_validator
import re

class User(BaseModel):
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    phone: str
    password: str

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        # Требование: начинается с +7, затем 10 цифр (всего 12 символов)
        if not re.match(r'^\+7\d{10}$', v):
            raise ValueError('Телефон должен начинаться с +7 и содержать 10 цифр (например +71234567890)')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Пароль должен содержать не менее 8 символов')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать минимум одну заглавную букву')
        if not re.search(r'[$%&!:]', v):
            raise ValueError('Пароль должен содержать минимум один специальный символ ($%&!:)')
        # Разрешены только латинские буквы (верх/нижний регистр), цифры и указанные спецсимволы
        if not re.match(r'^[A-Za-z0-9$%&!:]+$', v):
            raise ValueError('Пароль может содержать только латинские буквы, цифры и символы $%&!::')
        return v

class DisplayUser(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    model_config = ConfigDict(from_attributes=True)


class DisplayRole(DisplayUser):
    role: Role
