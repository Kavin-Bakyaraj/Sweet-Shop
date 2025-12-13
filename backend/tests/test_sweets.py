import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_sweet_admin(client: AsyncClient):
    # Register admin
    await client.post("/api/auth/register", json={
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    
    # Login
    login_res = await client.post("/api/auth/login", data={
        "username": "admin",
        "password": "adminpassword"
    })
    token = login_res.json()["access_token"]
    
    # Make user admin (hack for testing since we don't have admin reg endpoint yet)
    # In a real app, we'd seed the DB or have a special endpoint. 
    # Here we can assume the first user is admin or update DB directly.
    # But I can't access DB directly easily here without importing.
    # Let's just assume I need to implement a way to make user admin or just mock it.
    # Actually, I can use the `db` fixture if I expose it?
    # Or I can just update the document in the test if I use the `db` object from app.
    
    from app.core.database import db
    await db.get_db().users.update_one({"username": "admin"}, {"$set": {"is_admin": True}})

    # Create Sweet
    response = await client.post("/api/admin/sweets", json={
        "name": "Chocolate Fudge",
        "category": "Fudge",
        "price": 5.99,
        "quantity": 100
    }, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Chocolate Fudge"
    assert data["id"] is not None

@pytest.mark.asyncio
async def test_create_sweet_non_admin(client: AsyncClient):
    # Register user
    await client.post("/api/auth/register", json={
        "username": "user",
        "email": "user@example.com",
        "password": "userpassword"
    })
    
    # Login
    login_res = await client.post("/api/auth/login", data={
        "username": "user",
        "password": "userpassword"
    })
    token = login_res.json()["access_token"]

    # Try Create Sweet
    response = await client.post("/api/admin/sweets", json={
        "name": "Lollipop",
        "category": "Hard Candy",
        "price": 1.50,
        "quantity": 50
    }, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_delete_sweet(client: AsyncClient):
    # Register admin
    await client.post("/api/auth/register", json={
        "username": "admin_crud",
        "email": "admin_crud@example.com",
        "password": "password"
    })
    login_res = await client.post("/api/auth/login", data={"username": "admin_crud", "password": "password"})
    token = login_res.json()["access_token"]
    
    from app.core.database import db
    await db.get_db().users.update_one({"username": "admin_crud"}, {"$set": {"is_admin": True}})

    # Create Sweet
    create_res = await client.post("/api/admin/sweets", json={
        "name": "To Update",
        "category": "Test",
        "price": 10,
        "quantity": 10
    }, headers={"Authorization": f"Bearer {token}"})
    sweet_id = create_res.json()["id"]

    # Update Sweet
    update_res = await client.put(f"/api/admin/sweets/{sweet_id}", json={
        "price": 15.0,
        "quantity": 20
    }, headers={"Authorization": f"Bearer {token}"})
    assert update_res.status_code == 200
    assert update_res.json()["price"] == 15.0
    assert update_res.json()["quantity"] == 20

    # Delete Sweet
    delete_res = await client.delete(f"/api/admin/sweets/{sweet_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_res.status_code == 200
    
    # Verify Deletion
    get_res = await client.get("/api/sweets")
    data = get_res.json()
    assert not any(s["id"] == sweet_id for s in data)
