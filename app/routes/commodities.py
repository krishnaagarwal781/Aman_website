from fastapi import FastAPI, HTTPException, APIRouter
from bson import ObjectId

from app.models.models import *
from app.config.private import *

# Define Pydantic models for request and response


# Initialize FastAPI app
commodityRouter = APIRouter()

# Commodity endpoints
@commodityRouter.post("/commodity/create-commodity", response_model=Commodity, tags=['Commodity Routes'])
async def create_commodity(commodity: Commodity):
    result = commodities_collection.insert_one(commodity.dict())
    created_commodity = commodities_collection.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_commodity

@commodityRouter.patch("/commodity/edit-commodity/{commodity_id}", response_model=Commodity, tags=['Commodity Routes'])
async def edit_commodity(commodity_id: str, commodity_data: Commodity):
    commodities_collection.update_one({"_id": ObjectId(commodity_id)}, {"$set": commodity_data.dict()})
    updated_commodity = commodities_collection.find_one({"_id": ObjectId(commodity_id)}, {"_id": 0})
    if updated_commodity:
        return updated_commodity
    else:
        raise HTTPException(status_code=404, detail="Commodity not found")

@commodityRouter.post("/commodity/delete-commodity/{commodity_id}", tags=['Commodity Routes'])
async def delete_commodity(commodity_id: str):
    result = commodities_collection.delete_one({"_id": ObjectId(commodity_id)})
    if result.deleted_count == 1:
        return {"message": "Commodity deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Commodity not found")

@commodityRouter.get("/commodity/get-all-commodity", response_model=list[Commodity], tags=['Commodity Routes'])
async def get_all_commodities():
    commodities = list(commodities_collection.find({}, {"_id": 0}))
    return commodities
