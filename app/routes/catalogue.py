from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]

# Define Pydantic models for request and response


# Initialize FastAPI app
app = FastAPI()

# Catalogue endpoints
@app.get("/all-catalogue", response_model=list[Catalogue])
async def get_all_catalogues():
    coll = db["catalogues"]
    catalogues = list(coll.find({}, {"_id": 0}))
    return catalogues

@app.post("/create-catalogue", response_model=Catalogue)
async def create_catalogue(catalogue: Catalogue):
    coll = db["catalogues"]
    result = coll.insert_one(catalogue.dict())
    created_catalogue = coll.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_catalogue

@app.patch("/edit-catalogue/{catalogue_id}", response_model=Catalogue)
async def edit_catalogue(catalogue_id: str, catalogue_data: Catalogue):
    coll = db["catalogues"]
    coll.update_one({"_id": ObjectId(catalogue_id)}, {"$set": catalogue_data.dict()})
    updated_catalogue = coll.find_one({"_id": ObjectId(catalogue_id)}, {"_id": 0})
    if updated_catalogue:
        return updated_catalogue
    else:
        raise HTTPException(status_code=404, detail="Catalogue not found")

@app.post("/delete-catalogue/{catalogue_id}")
async def delete_catalogue(catalogue_id: str):
    coll = db["catalogues"]
    result = coll.delete_one({"_id": ObjectId(catalogue_id)})
    if result.deleted_count == 1:
        return {"message": "Catalogue deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Catalogue not found")
