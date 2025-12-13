import asyncio
from app.core.database import db

async def seed_sweets():
    print("Connecting to database...")
    db.connect()
    database = db.get_db()
    
    sweets_data = [
        {
            "name": "Motichoor Laddu",
            "category": "Laddu",
            "price": 15.00,
            "quantity": 100,
            "description": "Delicious gram flour balls fried in ghee."
        },
        {
            "name": "Kaju Katli",
            "category": "Burfi",
            "price": 25.00,
            "quantity": 50,
            "description": "Rich cashew fudge with silver leaf."
        },
        {
            "name": "Mysore Pak",
            "category": "Ghee Sweets",
            "price": 20.00,
            "quantity": 75,
            "description": "Melt-in-your-mouth ghee sweet from Mysore."
        },
        {
            "name": "Jalebi",
            "category": "Syrup Sweets",
            "price": 10.00,
            "quantity": 150,
            "description": "Crispy, orange spirals soaked in sugar syrup."
        },
        {
            "name": "Gulab Jamun",
            "category": "Syrup Sweets",
            "price": 12.00,
            "quantity": 120,
            "description": "Soft milk solid balls soaked in rose-flavored syrup."
        },
        {
            "name": "Rasgulla",
            "category": "Bengali Sweets",
            "price": 14.00,
            "quantity": 80,
            "description": "Spongy cottage cheese balls in light syrup."
        }
    ]

    print("Seeding sweets...")
    for sweet in sweets_data:
        existing = await database.sweets.find_one({"name": sweet["name"]})
        if not existing:
            await database.sweets.insert_one(sweet)
            print(f"Added: {sweet['name']}")
        else:
            print(f"Skipped (already exists): {sweet['name']}")

    print("Seeding complete!")
    db.close()

if __name__ == "__main__":
    asyncio.run(seed_sweets())
