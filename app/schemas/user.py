from app.schemas.item import Item
from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    pass
