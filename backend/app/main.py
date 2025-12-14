from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import db
from app.modules.auth.router import router as auth_router
from app.modules.admin.router import router as admin_router
from app.modules.catalog.router import router as catalog_router
from app.modules.inventory.router import router as inventory_router
from app.modules.orders.router import router as orders_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    yield
    db.close()

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Sweet Shop API", lifespan=lifespan)

# CORS Configuration
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Render deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists
os.makedirs("static/images", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(catalog_router, prefix="/api")
app.include_router(inventory_router, prefix="/api")
app.include_router(orders_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Welcome to Sweet Shop API"}
