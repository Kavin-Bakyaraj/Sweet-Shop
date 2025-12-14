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

@pytest.fixture(scope="function")
async def token(client: AsyncClient):
    # Register
    user_data = {
        "username": "authtest",
        "email": "auth@test.com",
        "password": "password123"
    }
    await client.post("/api/auth/register", json=user_data)
    
    # Login
    response = await client.post("/api/auth/login", data={
        "username": "authtest",
        "password": "password123"
    })
    return response.json()["access_token"]

@pytest.fixture(scope="function")
async def admin_token(client: AsyncClient):
    # Create admin user directly in DB
    from app.core.security import get_password_hash
    
    admin_data = {
        "username": "admintest",
        "email": "admin@test.com",
        "hashed_password": get_password_hash("admin123"),
        "is_admin": True
    }
    
    # We need to access the DB directly. 
    # Since client fixture connects db, we can use db.get_db()
    await db.get_db().users.insert_one(admin_data)
    
    # Login
    response = await client.post("/api/auth/login", data={
        "username": "admintest",
        "password": "admin123"
    })
    return response.json()["access_token"]
