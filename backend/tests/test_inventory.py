import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_purchase_sweet(client: AsyncClient):
    # Setup: Admin creates sweet
    await client.post("/api/auth/register", json={"username": "admin_inv", "email": "admin_inv@example.com", "password": "password"})
    login_res = await client.post("/api/auth/login", data={"username": "admin_inv", "password": "password"})
    admin_token = login_res.json()["access_token"]
    
    from app.core.database import db
    await db.get_db().users.update_one({"username": "admin_inv"}, {"$set": {"is_admin": True}})

    create_res = await client.post("/api/admin/sweets", json={"name": "To Buy", "category": "Test", "price": 10, "quantity": 5}, headers={"Authorization": f"Bearer {admin_token}"})
    sweet_id = create_res.json()["id"]

    # Register User
    await client.post("/api/auth/register", json={"username": "buyer", "email": "buyer@example.com", "password": "password"})
    login_res = await client.post("/api/auth/login", data={"username": "buyer", "password": "password"})
    user_token = login_res.json()["access_token"]

    # Purchase
    response = await client.post(f"/api/inventory/sweets/{sweet_id}/purchase", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Purchase successful"
    
    # Verify Quantity
    get_res = await client.get("/api/sweets")
    sweet = next(s for s in get_res.json() if s["id"] == sweet_id)
    assert sweet["quantity"] == 4

@pytest.mark.asyncio
async def test_purchase_out_of_stock(client: AsyncClient):
    # Setup: Admin creates sweet with 0 qty
    await client.post("/api/auth/register", json={"username": "admin_oos", "email": "admin_oos@example.com", "password": "password"})
    login_res = await client.post("/api/auth/login", data={"username": "admin_oos", "password": "password"})
    admin_token = login_res.json()["access_token"]
    
    from app.core.database import db
    await db.get_db().users.update_one({"username": "admin_oos"}, {"$set": {"is_admin": True}})

    create_res = await client.post("/api/admin/sweets", json={"name": "Empty", "category": "Test", "price": 10, "quantity": 0}, headers={"Authorization": f"Bearer {admin_token}"})
    sweet_id = create_res.json()["id"]

    # Register User
    await client.post("/api/auth/register", json={"username": "buyer2", "email": "buyer2@example.com", "password": "password"})
    login_res = await client.post("/api/auth/login", data={"username": "buyer2", "password": "password"})
    user_token = login_res.json()["access_token"]

    # Purchase
    response = await client.post(f"/api/inventory/sweets/{sweet_id}/purchase", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 400
    assert "Out of stock" in response.json()["detail"]

@pytest.mark.asyncio
async def test_restock_sweet(client: AsyncClient):
    # Setup: Admin creates sweet
    await client.post("/api/auth/register", json={"username": "admin_restock", "email": "admin_restock@example.com", "password": "password"})
    login_res = await client.post("/api/auth/login", data={"username": "admin_restock", "password": "password"})
    admin_token = login_res.json()["access_token"]
    
    from app.core.database import db
    await db.get_db().users.update_one({"username": "admin_restock"}, {"$set": {"is_admin": True}})

    create_res = await client.post("/api/admin/sweets", json={"name": "To Restock", "category": "Test", "price": 10, "quantity": 5}, headers={"Authorization": f"Bearer {admin_token}"})
    sweet_id = create_res.json()["id"]

    # Restock
    response = await client.post(f"/api/inventory/sweets/{sweet_id}/restock", json={"quantity": 10}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["quantity"] == 15
