from app.schemas.item import Item
from pydantic import BaseModel, EmailStr, ConfigDict
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

    # class Config:
    #     orm_mode = True
# Additional properties to return via API


class User(UserInDBBase):
    pass
