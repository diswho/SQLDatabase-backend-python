from fastapi import Depends, APIRouter, HTTPException
from app import schemas, model
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_superuser
from app.crud import crud_user
from typing import Any, List

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: model.User = Depends(get_current_active_superuser)):
    print("--- User: ", user)
    db_user = crud_user.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: model.User = Depends(get_current_active_superuser)):
    users = crud_user.get_users(db=db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db),
              current_user: model.User = Depends(get_current_active_superuser)):
    db_user = crud_user.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
