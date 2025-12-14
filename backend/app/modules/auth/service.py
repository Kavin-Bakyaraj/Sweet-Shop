from app.core.database import db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.modules.auth.schemas import UserCreate, Token, UserUpdate
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

async def create_user(user: UserCreate):
    database = db.get_db()
    existing_user = await database.users.find_one({"$or": [{"username": user.username}, {"email": user.email}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    user_dict["is_admin"] = False
    
    result = await database.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict

async def authenticate_user(form_data: OAuth2PasswordRequestForm):
    database = db.get_db()
    user = await database.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

async def update_user_profile(current_username: str, user_update: UserUpdate):
    database = db.get_db()
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]
        
    if not update_data:
        return await database.users.find_one({"username": current_username})

    await database.users.update_one({"username": current_username}, {"$set": update_data})
    
    # Return updated user
    # If username was changed, we need to query by new username, else old one
    new_username = update_data.get("username", current_username)
    updated_user = await database.users.find_one({"username": new_username})
    updated_user["id"] = str(updated_user["_id"])
    return updated_user
