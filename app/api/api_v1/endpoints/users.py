from fastapi import Body, Depends, APIRouter, HTTPException
from app import schemas, model
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_superuser, get_current_active_user
from app.crud import crud_user
from typing import Any, List
from pydantic.networks import EmailStr
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: model.User = Depends(get_current_active_superuser)):
    print("--- User: ", user)
    db_user = crud_user.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               current_user: model.User = Depends(get_current_active_superuser)):
    users = crud_user.get_users(db=db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: model.User = Depends(get_current_active_user)):
    user = crud_user.get_user(db=db, user_id=user_id)
    if user == current_user:
        return user
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.get("/me/", response_model=schemas.User)
def read_user_me(
        db: Session = Depends(get_db),
        current_user: model.User = Depends(get_current_active_user)) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me/", response_model=schemas.User)
def update_user_me(
    db: Session = Depends(get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: model.User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    # user_in = schemas.UserInDB(**current_user_data)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    # print("======== current_user_data:",current_user_data)
    # print("======== user_in:",user_in)
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: model.User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update a user.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud_user.update(db, db_obj=user, obj_in=user_in)
    return user
