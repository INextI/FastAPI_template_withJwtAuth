from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from ..config import settings

class UserBase(BaseModel):
    nickname: str
    email: EmailStr

class UserLogin(BaseModel):
    password: str
    email: EmailStr

class UserCreate(UserBase):
    first_name: str = Field(min_length=2, max_length=50)
    second_name: str = Field(min_length=2, max_length=50)
    avatar_img: Optional[str] = None
    password: str = Field(min_length=2, max_length=100)
    nickname: str = Field(min_length=2, max_length=50)

class UserCreateResponse(UserBase):
    first_name: str
    second_name: str
    avatar_img: str

class UserGet(UserBase):
    id: int
    first_name: str
    second_name: str
    avatar_img: Optional[str] = None

    class Config:
        from_attributes = True