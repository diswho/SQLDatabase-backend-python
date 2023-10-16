from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.model.user import User
from app import schemas
from app.core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, schemas.UserCreate, schemas.UserUpdate]):
    def get_user(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user: schemas.UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = User(
            email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(db=db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser
