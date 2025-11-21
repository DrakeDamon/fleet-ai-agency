from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# check_same_thread is needed only for SQLite, ignored by Postgres
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(settings.DATABASE_URL, echo=False, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
