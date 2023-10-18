from fastapi import Depends, APIRouter
from app import schemas, model
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_superuser
from app.crud import crud_item
from typing import Any, List

router = APIRouter()


@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(    
    user_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_active_superuser)
):
    return crud_item.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/", response_model=List[schemas.Item])
def read_items(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: model.User = Depends(get_current_active_superuser)):
    items = crud_item.get_items(db, skip=skip, limit=limit)
    return items
