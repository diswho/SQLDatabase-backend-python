from fastapi import Depends, APIRouter
from app import schemas
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import crud_item
from typing import Any, List

router = APIRouter()


@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud_item.create_user_item(db=db, item=item, user_id=user_id)
    # return user.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud_item.get_items(db, skip=skip, limit=limit)
    return items
