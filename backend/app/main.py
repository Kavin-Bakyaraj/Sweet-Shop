from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import db
from app.modules.auth.router import router as auth_router
from app.modules.admin.router import router as admin_router
from app.modules.catalog.router import router as catalog_router
from app.modules.inventory.router import router as inventory_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    yield
    db.close()

app = FastAPI(title="Sweet Shop API", lifespan=lifespan)

app.include_router(auth_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(catalog_router, prefix="/api")
app.include_router(inventory_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Sweet Shop API"}
