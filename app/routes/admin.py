from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from app.config.private import *
from app.models.models import *
from app.schemas.schemas import *
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]

app = FastAPI()

# Admin endpoints
@app.post("/admin-register", response_model=AdminDetails)
async def admin_register(admin: AdminRegister):
    coll = db["admins"]
    result = coll.insert_one(admin.dict())
    created_admin = coll.find_one({"_id": result.inserted_id})
    return {**created_admin, "user_id": str(created_admin["_id"])}

@app.post("/admin-login", response_model=AdminDetails)
async def admin_login(admin_login: AdminLogin):
    coll = db["admins"]
    admin = coll.find_one({"email": admin_login.email, "password": admin_login.password})
    if admin:
        return {**admin, "user_id": str(admin["_id"])}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/get-admin-details", response_model=AdminDetails)
async def get_admin_details(email: str, password: str):
    coll = db["admins"]
    admin = coll.find_one({"email": email, "password": password})
    if admin:
        return {**admin, "user_id": str(admin["_id"])}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Update endpoints
@app.get("/all-updates", response_model=list[Update])
async def get_all_updates():
    coll = db["updates"]
    updates = list(coll.find({}, {"_id": 0}))
    return updates

@app.post("/create-update", response_model=Update)
async def create_update(update: Update):
    coll = db["updates"]
    result = coll.insert_one(update.dict())
    created_update = coll.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_update

@app.patch("/edit-update/{update_id}", response_model=Update)
async def edit_update(update_id: str, update_data: Update):
    coll = db["updates"]
    coll.update_one({"_id": ObjectId(update_id)}, {"$set": update_data.dict()})
    updated_update = coll.find_one({"_id": ObjectId(update_id)}, {"_id": 0})
    if updated_update:
        return updated_update
    else:
        raise HTTPException(status_code=404, detail="Update not found")

@app.post("/delete-update/{update_id}")
async def delete_update(update_id: str):
    coll = db["updates"]
    result = coll.delete_one({"_id": ObjectId(update_id)})
    if result.deleted_count == 1:
        return {"message": "Update deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Update not found")
