import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import db
from app.core.config import settings

# Override settings for testing
settings.DATABASE_NAME = "sweet_shop_test"

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="function")
async def client():
    # Connect to test database
    db.connect()
    
    # Create async client
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    # Cleanup and close
    await db.get_db().client.drop_database(settings.DATABASE_NAME)
    db.close()
