import asyncio
from app.core.database import db

async def fix_users():
    print("Connecting to database...")
    db.connect()
    database = db.get_db()
    
    print("Fixing user documents...")
    users = await database.users.find({}).to_list(length=1000)
    
    for user in users:
        username = user.get("username", "unknown")
        print(f"Checking user: {username}")
        
        if "password" in user and "hashed_password" not in user:
            print(f"  - Migrating 'password' to 'hashed_password' for {username}")
            await database.users.update_one(
                {"_id": user["_id"]},
                {
                    "$set": {"hashed_password": user["password"]},
                    "$unset": {"password": ""}
                }
            )
            print("  - Done.")
        elif "hashed_password" not in user:
             print(f"  - WARNING: User {username} has no password field!")
        else:
            print(f"  - User {username} is already correct.")

    print("Finished fixing users.")
    db.close()

if __name__ == "__main__":
    asyncio.run(fix_users())
