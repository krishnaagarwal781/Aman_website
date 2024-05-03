from fastapi import FastAPI, HTTPException, APIRouter
from bson import ObjectId

from app.models.models import *
from app.config.private import *

tradeshowRouter = APIRouter()

# Tradeshow endpoints
@tradeshowRouter.get("/tradeshow/all-tradeshow", response_model=list[Tradeshow], tags=['Tradeshow Routes'])
async def get_all_tradeshows():
    tradeshows = list(tradeshows_collection.find({}, {"_id": 0}))
    return tradeshows

@tradeshowRouter.post("/tradeshow/create-tradeshow", response_model=Tradeshow, tags=['Tradeshow Routes'])
async def create_tradeshow(tradeshow: Tradeshow):
    result = tradeshows_collection.insert_one(tradeshow.dict())
    created_tradeshow = tradeshows_collection.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_tradeshow

@tradeshowRouter.patch("/tradeshow/edit-tradeshow/{tradeshow_id}", response_model=Tradeshow, tags=['Tradeshow Routes'])
async def edit_tradeshow(tradeshow_id: str, tradeshow_data: Tradeshow):
    tradeshows_collection.update_one({"_id": ObjectId(tradeshow_id)}, {"$set": tradeshow_data.dict()})
    updated_tradeshow = tradeshows_collection.find_one({"_id": ObjectId(tradeshow_id)}, {"_id": 0})
    if updated_tradeshow:
        return updated_tradeshow
    else:
        raise HTTPException(status_code=404, detail="Tradeshow not found")

@tradeshowRouter.post("/tradeshow/delete-tradeshow/{tradeshow_id}", tags=['Tradeshow Routes'])
async def delete_tradeshow(tradeshow_id: str):
    result = tradeshows_collection.delete_one({"_id": ObjectId(tradeshow_id)})
    if result.deleted_count == 1:
        return {"message": "Tradeshow deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Tradeshow not found")
