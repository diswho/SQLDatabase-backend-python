from fastapi import Depends, APIRouter
from app.schemas.item import Item, ItemCreate
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import crud

router = APIRouter()


@router.post("/users/{user_id}/items/", response_model=Item)
def create_item_for_user(
    user_id: int, item: ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
