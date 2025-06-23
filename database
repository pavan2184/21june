from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = MongoClient(MONGO_URL)
db = client["myapp_db"]

users_collection = db["users"]
movies_collection = db["movies"]
