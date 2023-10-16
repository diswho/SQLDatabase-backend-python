from sqlalchemy.orm import Session

from app import crud
# from app.schemas import schemas
from app.schemas.user import UserCreate
# from app.model import models
from app.db.base import Base
from app.db.session import engine
# from app.db.database import engine


def init_db(db: Session) -> None:
    FIRST_SUPERUSER = "vientiane@vientiane.com"
    FIRST_SUPERUSER_PASSWORD = "vientiane"
    Base.metadata.create_all(bind=engine)
    user = crud.user.get_user_by_email(db, email=FIRST_SUPERUSER)
    # user = crud.get_user_by_email(db, email=FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=FIRST_SUPERUSER,
            password=FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create_user(db=db, user=user_in)
        # user = crud.create_user(db=db, user=user_in)
    else:
        print("====== User Exist")
    #     # user = crud.user.create(db, obj_in=user_in)  # noqa: F841
