import time, pymongo, datetime, pytz
from pymongo import MongoClient

mongo_url = "mongodb+srv://anuragbiswal2002:AGRRsC7YUmKGZ7vi@cluster0.vkhfdti.mongodb.net/"
client = MongoClient(mongo_url)

db = client["Aman_website"]

admin_collection = db["admins"]
update_collection = db["updates"]
business_forms_collection = db["business_forms"]
catalogues_collection = db["catalogues"]
categories_collection = db["categories"]
commodities_collection = db["commodities"]
contact_forms_collection = db["contact_forms"]
gallery_collection = db["gallery"]
testimonials_collection = db["testimonials"]
tradeshows_collection = db["tradeshows"]