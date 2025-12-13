import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password" not in data

@pytest.mark.asyncio
async def test_register_existing_user(client: AsyncClient):
    # Register first time
    await client.post("/api/auth/register", json={
        "username": "duplicate",
        "email": "dup@example.com",
        "password": "password123"
    })
    
    # Register second time
    response = await client.post("/api/auth/register", json={
        "username": "duplicate",
        "email": "dup@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
