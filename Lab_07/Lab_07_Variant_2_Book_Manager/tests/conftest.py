import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from book_manager.models import Base

@pytest.fixture
def session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _record):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as db:
        yield db
    Base.metadata.drop_all(engine)
    engine.dispose()
