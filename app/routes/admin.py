from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from bson import ObjectId
from app.config.private import *
from app.models.models import *
from passlib.context import CryptContext

adminRouter = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Admin endpoints
@adminRouter.post("/admin/admin-register", tags=['Admin Routes'])
async def admin_register(admin: AdminRegister):
    adminPresent = admin_collection.find_one({"email": admin.email})  # Check if username is already registered
    if adminPresent:
        raise HTTPException(status_code=400, detail="Admin already exists!")
    hashed_password = pwd_context.hash(admin.password)
    admin.password = hashed_password  # Store the hashed password instead of the plain one
    result = admin_collection.insert_one(admin.model_dump())
    return JSONResponse(status_code=201, content={"message": "New Admin Created.", "admin_id": str(result.inserted_id)})


@adminRouter.post("/admin/admin-login", tags=['Admin Routes'])
async def admin_login(email:str, password:str):
    adminPresent = admin_collection.find_one({"email": email})
    if adminPresent:
        if pwd_context.verify(password, adminPresent["password"]):
            return {"message": "Logged In Successfully!", "admin_id": str(adminPresent['_id'])}
        else:
            raise HTTPException(status_code=400, detail="Wrong Password!")
    else:
        raise HTTPException(status_code=400, detail="Wrong Email or Password")

@adminRouter.get("/admin/get-admin-details",  tags=['Admin Routes'])
async def get_admin_details(email: str, password: str):
    admin = admin_collection.find_one({"email": email, "password": password})
    if admin:
        return {**admin, "user_id": str(admin["_id"])}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")