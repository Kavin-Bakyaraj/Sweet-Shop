from fastapi import APIRouter, status, Depends, UploadFile, File, HTTPException
from app.modules.catalog.schemas import SweetCreate, SweetResponse, SweetUpdate
from app.modules.admin.service import create_sweet, update_sweet, delete_sweet
from app.core.dependencies import get_current_admin


router = APIRouter(prefix="/admin", tags=["Admin"])

from app.core.s3_service import s3_service

@router.post("/upload")
async def upload_image(file: UploadFile = File(...), admin=Depends(get_current_admin)):
    return {"url": await s3_service.upload_file(file)}

@router.post("/sweets", response_model=SweetResponse, status_code=status.HTTP_201_CREATED)
async def add_sweet(sweet: SweetCreate, admin=Depends(get_current_admin)):
    return await create_sweet(sweet)

@router.put("/sweets/{id}", response_model=SweetResponse)
async def edit_sweet(id: str, sweet: SweetUpdate, admin=Depends(get_current_admin)):
    return await update_sweet(id, sweet)

@router.delete("/sweets/{id}")
async def remove_sweet(id: str, admin=Depends(get_current_admin)):
    return await delete_sweet(id)
    return await delete_sweet(id)

from app.modules.admin.schemas import AdminUserCreate
from app.modules.admin.service import create_admin_user
from app.modules.auth.schemas import UserResponse

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add_admin_user(user: AdminUserCreate, admin=Depends(get_current_admin)):
    return await create_admin_user(user)
