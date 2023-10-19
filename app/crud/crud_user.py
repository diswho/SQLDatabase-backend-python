from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from app.model.user import User
from app.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from fastapi.encoders import jsonable_encoder


def create(db: Session, user: UserCreate) -> Optional[User]:
    db_user = User(email=user.email,
                   hashed_password=get_password_hash(user.password),
                   full_name=user.full_name,
                   is_superuser=user.is_superuser,)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def update(db: Session, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    if obj_in.password is not None:
        # if update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    obj_data = jsonable_encoder(db_obj)
    # if isinstance(obj_in, dict):
    #     update_data01 = obj_in
    # else:
    #     update_data01 = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    # return update(db, db_obj=db_obj, obj_in=update_data)


def authenticate(db: Session,  email: str, password: str) -> Optional[User]:
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def is_active(user: User) -> bool:
    return user.is_active


def is_superuser(user: User) -> bool:
    return user.is_superuser


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
