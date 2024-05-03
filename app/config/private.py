import time, pymongo, datetime, pytz
from pymongo import MongoClient

mongo_url = "mongodb://sniplyuser:NXy7R7wRskSrk3F2@ac-whear6l-shard-00-00.iwac6oj.mongodb.net:27017,ac-whear6l-shard-00-01.iwac6oj.mongodb.net:27017,ac-whear6l-shard-00-02.iwac6oj.mongodb.net:27017/?replicaSet=atlas-110fhx-shard-0&ssl=true&authSource=admin"
client = MongoClient(mongo_url)
db = client["Aman_website"]