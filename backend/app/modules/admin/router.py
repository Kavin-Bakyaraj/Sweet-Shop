from fastapi import APIRouter, status, Depends
from app.modules.catalog.schemas import SweetCreate, SweetResponse, SweetUpdate
from app.modules.admin.service import create_sweet, update_sweet, delete_sweet
from app.core.dependencies import get_current_admin

router = APIRouter(prefix="/admin/sweets", tags=["Admin"])

@router.post("", response_model=SweetResponse, status_code=status.HTTP_201_CREATED)
async def add_sweet(sweet: SweetCreate, admin=Depends(get_current_admin)):
    return await create_sweet(sweet)

@router.put("/{id}", response_model=SweetResponse)
async def edit_sweet(id: str, sweet: SweetUpdate, admin=Depends(get_current_admin)):
    return await update_sweet(id, sweet)

@router.delete("/{id}")
async def remove_sweet(id: str, admin=Depends(get_current_admin)):
    return await delete_sweet(id)
    return await delete_sweet(id)

from app.modules.admin.schemas import AdminUserCreate
from app.modules.admin.service import create_admin_user
from app.modules.auth.schemas import UserResponse

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add_admin_user(user: AdminUserCreate, admin=Depends(get_current_admin)):
    return await create_admin_user(user)
