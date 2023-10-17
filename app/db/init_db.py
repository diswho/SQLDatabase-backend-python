from sqlalchemy.orm import Session

from app.crud import crud_user
from app.schemas.user import UserCreate
from app.db.base import Base
from app.db.session import engine
from app.core.config import settings


def init_db(db: Session) -> None:
    settings.FIRST_SUPERUSER = "vientiane@vientiane.com"
    settings.FIRST_SUPERUSER_PASSWORD = "vientiane"
    Base.metadata.create_all(bind=engine)
    user = crud_user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        try:
            user = crud_user.create(db=db, user=user_in)
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
    else:
        print("====== User Exist")
