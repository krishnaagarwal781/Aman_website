from fastapi import HTTPException, APIRouter
from bson import ObjectId
from app.config.private import *
from app.models.models import *

updateRouter = APIRouter()


# Update endpoints
@updateRouter.get("/update/all-updates", response_model=list[Update], tags=['Update Routes'])
async def get_all_updates():
    updates = list(update_collection.find({}, {"_id": 0}))
    return updates

@updateRouter.post("/update/create-update", response_model=Update, tags=['Update Routes'])
async def create_update(update: Update):
    result = update_collection.insert_one(update.dict())
    created_update = update_collection.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_update

@updateRouter.patch("/update/edit-update/{update_id}", response_model=Update, tags=['Update Routes'])
async def edit_update(update_id: str, update_data: Update):
    update_collection.update_one({"_id": ObjectId(update_id)}, {"$set": update_data.dict()})
    updated_update = update_collection.find_one({"_id": ObjectId(update_id)}, {"_id": 0})
    if updated_update:
        return updated_update
    else:
        raise HTTPException(status_code=404, detail="Update not found")

@updateRouter.post("/update/delete-update/{update_id}", tags=['Update Routes'])
async def delete_update(update_id: str):
    result = update_collection.delete_one({"_id": ObjectId(update_id)})
    if result.deleted_count == 1:
        return {"message": "Update deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Update not found")
