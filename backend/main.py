# backend/main.py
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.trip_planner

@app.get("/health")
async def health_check():
    return {"status": "ok"}



@app.get("/test-mongo")
async def test_mongo():
    try:
        poi = db.pois.find_one({"city": "HAN"})
        if poi:
            # Convert ObjectId to string
            poi["_id"] = str(poi["_id"])
        return {"status": "success", "poi": poi}
    except Exception as e:
        return {"status": "error", "message": str(e)}