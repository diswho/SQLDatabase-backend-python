from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.model.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate
from app import schemas


class CRUDItem(CRUDBase[Item, schemas.ItemCreate, schemas.ItemUpdate]):
    def get_items(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Item).offset(skip).limit(limit).all()

    def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
        # item_in_data = jsonable_encoder(item)
        # db_item = Item(**item_in_data, owner_id=user_id)
        db_item = Item(**item.dict(), owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item


item = CRUDItem(Item)
