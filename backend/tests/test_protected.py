import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_protected_route_access(client: AsyncClient):
    # Try to access protected route without token
    response = await client.get("/api/auth/me")
    assert response.status_code == 401

    # Register user first
    await client.post("/api/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "password123"
    })

    # Login to get token
    login_response = await client.post("/api/auth/login", data={
        "username": "loginuser",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # Access with token
    response = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "loginuser"
