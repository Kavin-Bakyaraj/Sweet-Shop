import asyncio
from app.core.database import db
from app.core.security import get_password_hash
from app.core.config import Settings

async def seed_admin():
    print("Connecting to database...")
    db.connect()
    database = db.get_db()
    
    admin_username = "admin"
    admin_email = "admin@sweetshop.com"
    admin_password = "Admin@lalsweets9363" # Change this in production!

    print(f"Checking for existing admin user: {admin_username}")
    existing_admin = await database.users.find_one({"username": admin_username})
    
    hashed_password = get_password_hash(admin_password)
    
    if existing_admin:
        print("Admin user already exists. Updating password...")
        await database.users.update_one(
            {"username": admin_username},
            {"$set": {"hashed_password": hashed_password}}
        )
        print(f"Admin password updated successfully.")
    else:
        print("Creating admin user...")
        admin_user = {
            "username": admin_username,
            "email": admin_email,
            "hashed_password": hashed_password,
            "is_admin": True
        }
        await database.users.insert_one(admin_user)
        print(f"Admin user created successfully!")
        print(f"Username: {admin_username}")
        print(f"Password: {admin_password}")

    db.close()

if __name__ == "__main__":
    asyncio.run(seed_admin())
