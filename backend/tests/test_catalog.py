import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_sweets(client: AsyncClient):
    # Seed data (via admin endpoint)
    # Register admin
    await client.post("/api/auth/register", json={
        "username": "admin_cat",
        "email": "admin_cat@example.com",
        "password": "password"
    })
    login_res = await client.post("/api/auth/login", data={"username": "admin_cat", "password": "password"})
    token = login_res.json()["access_token"]
    
    # Make admin
    from app.core.database import db
    await db.get_db().users.update_one({"username": "admin_cat"}, {"$set": {"is_admin": True}})

    # Create sweets
    await client.post("/api/admin/sweets", json={"name": "Sweet A", "category": "Cat1", "price": 10, "quantity": 10}, headers={"Authorization": f"Bearer {token}"})
    await client.post("/api/admin/sweets", json={"name": "Sweet B", "category": "Cat2", "price": 20, "quantity": 5}, headers={"Authorization": f"Bearer {token}"})

    # List sweets (Public)
    response = await client.get("/api/sweets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

@pytest.mark.asyncio
async def test_search_sweets(client: AsyncClient):
    # Setup data
    # Register admin
    await client.post("/api/auth/register", json={
        "username": "admin_search",
        "email": "admin_search@example.com",
        "password": "password"
    })
    login_res = await client.post("/api/auth/login", data={"username": "admin_search", "password": "password"})
    token = login_res.json()["access_token"]
    
    from app.core.database import db
    await db.get_db().users.update_one({"username": "admin_search"}, {"$set": {"is_admin": True}})

    # Create sweets
    await client.post("/api/admin/sweets", json={"name": "Sweet A", "category": "Cat1", "price": 10, "quantity": 10}, headers={"Authorization": f"Bearer {token}"})
    await client.post("/api/admin/sweets", json={"name": "Sweet B", "category": "Cat2", "price": 20, "quantity": 5}, headers={"Authorization": f"Bearer {token}"})

    # Search by name
    response = await client.get("/api/sweets/search?q=Sweet A")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Sweet A"

    # Search by category
    response = await client.get("/api/sweets/search?category=Cat2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Sweet B"
