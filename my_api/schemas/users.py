import re
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('password')
    def secure_password(cls, v): #mínimo de 8 caracteres contendo: maiúsculas, minúsculas, números e caracteres especiais (!@#$%^&*()-_=+[]{}|\;:'",.<>?/~`)
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(pattern, v):
            raise ValueError('Senha insegura')
        return v


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @field_validator('password')
    def secure_password(cls, v): #mínimo de 8 caracteres contendo: maiúsculas, minúsculas, números e caracteres especiais (!@#$%^&*()-_=+[]{}|\;:'",.<>?/~`)
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(pattern, v):
            raise ValueError('Senha insegura')
        return v


class UserPublicSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class UserListPublicSchema(BaseModel):
    users: List[UserPublicSchema]


class UserPublicShortSchema(BaseModel):
    id: int
    username: str
