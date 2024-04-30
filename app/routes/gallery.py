from fastapi import FastAPI, HTTPException
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]

# Define Pydantic models for request and response


# Initialize FastAPI app
app = FastAPI()

# Gallery endpoints
@app.get("/all-gallery", response_model=list[Gallery])
async def get_all_gallery():
    coll = db["gallery"]
    galleries = list(coll.find({}, {"_id": 1, "gallery_title": 1, "images": 1}))
    return galleries

@app.post("/create-gallery", response_model=Gallery)
async def create_gallery(gallery: GalleryItem):
    coll = db["gallery"]
    result = coll.insert_one(gallery.dict())
    created_gallery = coll.find_one({"_id": result.inserted_id})
    return {**created_gallery, "_id": str(created_gallery["_id"])}

@app.patch("/edit-gallery/{gallery_id}", response_model=Gallery)
async def edit_gallery(gallery_id: str, gallery_data: GalleryItem):
    coll = db["gallery"]
    coll.update_one({"_id": ObjectId(gallery_id)}, {"$set": gallery_data.dict()})
    updated_gallery = coll.find_one({"_id": ObjectId(gallery_id)})
    if updated_gallery:
        return {**updated_gallery, "_id": str(updated_gallery["_id"])}
    else:
        raise HTTPException(status_code=404, detail="Gallery not found")

@app.post("/delete-gallery/{gallery_id}")
async def delete_gallery(gallery_id: str):
    coll = db["gallery"]
    result = coll.delete_one({"_id": ObjectId(gallery_id)})
    if result.deleted_count == 1:
        return {"message": "Gallery deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Gallery not found")
