from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.core.permissions import UserRole, Country


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    country: Country


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
    role: UserRole
    country: Country
