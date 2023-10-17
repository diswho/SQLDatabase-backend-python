from sqlalchemy.orm import Session

from app import crud
# from app.schemas import schemas
from app.schemas.user import UserCreate
# from app.model import models
from app.db.base import Base
from app.db.session import engine
# from app.db.database import engine
from app.core.config import settings


def init_db(db: Session) -> None:
    settings.FIRST_SUPERUSER = "vientiane@vientiane.com"
    settings.FIRST_SUPERUSER_PASSWORD = "vientiane"
    Base.metadata.create_all(bind=engine)
    user = crud.user.get_user_by_email(db, email=settings.FIRST_SUPERUSER)
    # user = crud.get_user_by_email(db, email=FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        try:
            user = crud.user.create_user(db=db, user=user_in)
        except TypeError:
            print("====== TypeError")
        except KeyError:
            print("====== KeyError")
        except NameError:
            print("====== NameError")
        except IndexError:
            print("====== IndexError")
        except MemoryError:
            print("====== MemoryError")
        except ValueError:
            print("====== ValueError")
        except:
            print("====== Error")

        # user = crud.create_user(db=db, user=user_in)
    else:
        print("====== User Exist")
    #     # user = crud.user.create(db, obj_in=user_in)  # noqa: F841
