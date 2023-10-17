from app.schemas.item import Item
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional,List


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []
    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    pass
