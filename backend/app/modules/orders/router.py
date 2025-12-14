from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user
from app.core.database import db
from app.modules.orders.schemas import OrderCreate, OrderResponse, OrderItemResponse
from app.modules.orders.models import OrderModel
from app.modules.auth.schemas import UserResponse
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, user: UserResponse = Depends(get_current_user)):
    database = db.get_db()
    total_price = 0
    order_items = []

    # Validate items and calculate total
    for item in order_data.items:
        sweet = await database.sweets.find_one({"_id": ObjectId(item.sweet_id)})
        if not sweet:
            raise HTTPException(status_code=404, detail=f"Sweet {item.sweet_id} not found")
        
        if sweet["quantity"] < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {sweet['name']}")
        
        total_price += sweet["price"] * item.quantity
        
        # Deduct stock
        await database.sweets.update_one(
            {"_id": ObjectId(item.sweet_id)},
            {"$inc": {"quantity": -item.quantity}}
        )
        
        order_items.append({
            "sweet_id": item.sweet_id,
            "name": sweet["name"],
            "price": sweet["price"],
            "quantity": item.quantity
        })

    # Create Order
    order_model = OrderModel(
        user_id=user.id,
        items=order_items,
        total_price=total_price
    )
    
    new_order = await database.orders.insert_one(order_model.to_dict())
    created_order = await database.orders.find_one({"_id": new_order.inserted_id})
    
    created_order["id"] = str(created_order["_id"])
    return created_order

@router.get("/me", response_model=list[OrderResponse])
async def get_my_orders(user: UserResponse = Depends(get_current_user)):
    database = db.get_db()
    cursor = database.orders.find({"user_id": user.id}).sort("created_at", -1)
    orders = await cursor.to_list(length=100)
    
    for order in orders:
        order["id"] = str(order["_id"])
        
    return orders
