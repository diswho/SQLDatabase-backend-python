from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.model.user import User
# from app.schemas.user import UserCreate, UserUpdate
from app import schemas


class CRUDUser(CRUDBase[User, schemas.UserCreate, schemas.UserUpdate]):
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(db: Session, user: schemas.UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = User(
            email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


user = CRUDUser
