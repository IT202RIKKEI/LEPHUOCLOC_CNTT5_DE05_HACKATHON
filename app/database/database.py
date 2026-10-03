from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = "mysql+pymysql://root:01884814110Loc*@localhost:3306/library_db"

Engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=Engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
