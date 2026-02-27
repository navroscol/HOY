from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings

engine = create_engine(settings.db_url, echo=False, connect_args={"check_same_thread": False} if settings.db_url.startswith("sqlite") else {})


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
