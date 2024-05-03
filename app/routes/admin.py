from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from bson import ObjectId
from app.config.private import *
from app.models.models import *

adminRouter = APIRouter()

# Admin endpoints
@adminRouter.post("/admin/admin-register", response_model=AdminDetails, tags=['Admin Routes'])
async def admin_register(admin: AdminRegister):
    adminPresent = admin_collection.find_one({"admin_username": admin.admin_username})  # Check if username is already registered
    if adminPresent:
        raise HTTPException(status_code=400, detail="Admin already exists!")
    result = admin_collection.insert_one(admin.dict())
    created_admin = admin_collection.find_one({"_id": result.inserted_id})
    return {**created_admin, "user_id": str(created_admin["_id"])}

@adminRouter.post("/admin/admin-login", response_model=AdminDetails, tags=['Admin Routes'])
async def admin_login(admin_login: AdminLogin):
    admin = admin_collection.find_one({"email": admin_login.email, "password": admin_login.password})
    if admin:
        return {**admin, "user_id": str(admin["_id"])}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@adminRouter.get("/admin/get-admin-details", response_model=AdminDetails, tags=['Admin Routes'])
async def get_admin_details(email: str, password: str):
    admin = admin_collection.find_one({"email": email, "password": password})
    if admin:
        return {**admin, "user_id": str(admin["_id"])}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")