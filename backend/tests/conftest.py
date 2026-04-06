from app.main import app
from app.core.database import Base, SessionLocal, engine, get_db
import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure tests use an isolated SQLite database before app imports.
os.environ["DATABASE_URL"] = "sqlite:///./test_finance.db"
os.environ["APP_ENV"] = "test"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["CORS_ALLOW_ORIGINS"] = "http://localhost:3000"
TEST_DB_PATH = Path("test_finance.db")

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db_file():
    yield
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
@pytest.fixture
def client():
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
