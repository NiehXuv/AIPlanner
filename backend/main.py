# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, model_validator
from typing import Dict
from utils import fetch_pois
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pymongo
import logging
from bson.objectid import ObjectId
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import traceback

# Import components
from components.vector import interests_to_vector
from components.plan_generator import generate_plan_with_gemini
from components.clustering import cluster_pois
from components.mock_data import mock_hotels
from data.interests import interests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
logging.info(f"Loaded environment variables")

# Initialize FastAPI app
app = FastAPI()

# Initialize MongoDB client
mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["trip_planner"]

# Test MongoDB connection
try:
    mongo_client.server_info()
    logging.info("MongoDB Atlas connection successful")
except Exception as e:
    logging.error(f"MongoDB Atlas connection failed: {str(e)}")
    raise

# Initialize OpenAI client (not used for now)
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Pydantic model for request body
class PlanRequest(BaseModel):
    location: str
    start_date: str
    days: int
    interests: Dict[str, float]
    budget: float

    @model_validator(mode="before")
    @classmethod
    def check_interests(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        interests = data.get("interests", {})
        if not isinstance(interests, dict):
            raise ValueError("Interests must be a dictionary")
        
        valid_interests = set(interests)
        for interest in list(interests.keys()):
            if interest not in valid_interests:
                raise ValueError(f"Invalid interest: {interest}. Must be one of {valid_interests}")
            if interest == "ArtAndCulture":
                interests["Art & Culture"] = interests.pop(interest)
        data["interests"] = interests
        return data

# Endpoints
@app.post("/generate-plan")
async def generate_plan(request: PlanRequest):
    try:
        city_coordinates = {
            "Paris": {"iata": "PAR", "lat": 48.8566, "lon": 2.3522},
            "Tokyo": {"iata": "TYO", "lat": 35.6762, "lon": 139.6503},
            "Barcelona": {"iata": "BCN", "lat": 41.3851, "lon": 2.1734},
            "New York": {"iata": "NYC", "lat": 40.7128, "lon": -74.0060},
            "London": {"iata": "LON", "lat": 51.5074, "lon": -0.1278},
            "Rome": {"iata": "ROM", "lat": 41.9028, "lon": 12.4964},
            "Sydney": {"iata": "SYD", "lat": -33.8688, "lon": 151.2093},
            "Dubai": {"iata": "DXB", "lat": 25.2048, "lon": 55.2708},
            "Singapore": {"iata": "SIN", "lat": 1.3521, "lon": 103.8198},
            "Cape Town": {"iata": "CPT", "lat": -33.9249, "lon": 18.4241},
            "Rio de Janeiro": {"iata": "RIO", "lat": -22.9068, "lon": -43.1729},
            "Bangkok": {"iata": "BKK", "lat": 13.7563, "lon": 100.5018},
            "Istanbul": {"iata": "IST", "lat": 41.0082, "lon": 28.9784},
            "Seoul": {"iata": "SEL", "lat": 37.5665, "lon": 126.9780},
            "Amsterdam": {"iata": "AMS", "lat": 52.3676, "lon": 4.9041},
            "Prague": {"iata": "PRG", "lat": 50.0755, "lon": 14.4378},
            "Vienna": {"iata": "VIE", "lat": 48.2082, "lon": 16.3738},
            "San Francisco": {"iata": "SFO", "lat": 37.7749, "lon": -122.4194},
            "Kyoto": {"iata": "KIX", "lat": 35.0116, "lon": 135.7681},
            "Marrakech": {"iata": "RAK", "lat": 31.6295, "lon": -7.9811},
            "Edinburgh": {"iata": "EDI", "lat": 55.9533, "lon": -3.1883},
            "Havana": {"iata": "HAV", "lat": 23.1136, "lon": -82.3666}
        }
        city_info = city_coordinates.get(request.location)
        if not city_info:
            raise HTTPException(status_code=400, detail="Unsupported location")

        pois = await fetch_pois(city_info["iata"])
        logging.info(f"Fetched POIs for {request.location}: {pois}")

        user_vector = interests_to_vector(request.interests)
        logging.info(f"User interests vector: {user_vector}")

        # Filter POIs based on user interests
        filtered_pois = []
        similarity_threshold = 0.3
        for poi in pois:
            poi_interests = poi.get("interests", {})
            logging.info(f"POI {poi['name']} interests: {poi_interests}")
            poi_vector = interests_to_vector(poi_interests)
            logging.info(f"POI {poi['name']} vector: {poi_vector}")
            similarity = cosine_similarity([user_vector], [poi_vector])[0][0]
            logging.info(f"Similarity between user and POI {poi['name']}: {similarity}")
            if similarity >= similarity_threshold:
                poi["similarity"] = similarity
                filtered_pois.append(poi)

        filtered_pois.sort(key=lambda x: x["similarity"], reverse=True)
        logging.info(f"Filtered POIs: {filtered_pois}")

        if not filtered_pois:
            raise HTTPException(status_code=404, detail="No points of interest match your preferences")

        # Cluster POIs and assign to days
        daily_pois = cluster_pois(filtered_pois, days=request.days)
        logging.info(f"Daily POIs (names only for logging): {[[poi['name'] for poi in cluster] for cluster in daily_pois]}")
        logging.info(f"Daily POIs (full structure): {daily_pois}")

        # Generate the plan with Gemini
        plan_data = await generate_plan_with_gemini(
            request.location,
            request.start_date,
            request.days,
            request.interests,
            request.budget,
            daily_pois
        )

        plan_doc = {
            "location": request.location,
            "start_date": request.start_date,
            "days": request.days,
            "interests": request.interests,
            "budget": request.budget,
            "plan": plan_data["plan"],
            "hotel": plan_data["Hotel"]
        }
        result = db.plans.insert_one(plan_doc)
        plan_id = str(result.inserted_id)
        logging.info(f"Stored plan with plan_id: {plan_id}")

        return {"plan_id": plan_id, "plan": plan_data}
    except Exception as e:
        logging.error(f"Error in /generate-plan: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error generating plan: {str(e)}")

@app.post("/edit-plan")
async def edit_plan(plan_id: str, request: PlanRequest):
    try:
        # Validate plan_id
        if not ObjectId.is_valid(plan_id):
            raise HTTPException(status_code=400, detail="Invalid plan_id")

        # Fetch the existing plan
        plan = db.plans.find_one({"_id": ObjectId(plan_id)})
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")

        # Validate location (must match the original plan)
        if request.location != plan["location"]:
            raise HTTPException(status_code=400, detail="Location cannot be changed")

        # Fetch POIs for the city
        city_coordinates = {
            "Paris": {"iata": "PAR", "lat": 48.8566, "lon": 2.3522},
            "Tokyo": {"iata": "TYO", "lat": 35.6762, "lon": 139.6503},
            "Barcelona": {"iata": "BCN", "lat": 41.3851, "lon": 2.1734},
            "New York": {"iata": "NYC", "lat": 40.7128, "lon": -74.0060},
            "London": {"iata": "LON", "lat": 51.5074, "lon": -0.1278},
            "Rome": {"iata": "ROM", "lat": 41.9028, "lon": 12.4964},
            "Sydney": {"iata": "SYD", "lat": -33.8688, "lon": 151.2093},
            "Dubai": {"iata": "DXB", "lat": 25.2048, "lon": 55.2708},
            "Singapore": {"iata": "SIN", "lat": 1.3521, "lon": 103.8198},
            "Cape Town": {"iata": "CPT", "lat": -33.9249, "lon": 18.4241},
            "Rio de Janeiro": {"iata": "RIO", "lat": -22.9068, "lon": -43.1729},
            "Bangkok": {"iata": "BKK", "lat": 13.7563, "lon": 100.5018},
            "Istanbul": {"iata": "IST", "lat": 41.0082, "lon": 28.9784},
            "Seoul": {"iata": "SEL", "lat": 37.5665, "lon": 126.9780},
            "Amsterdam": {"iata": "AMS", "lat": 52.3676, "lon": 4.9041},
            "Prague": {"iata": "PRG", "lat": 50.0755, "lon": 14.4378},
            "Vienna": {"iata": "VIE", "lat": 48.2082, "lon": 16.3738},
            "San Francisco": {"iata": "SFO", "lat": 37.7749, "lon": -122.4194},
            "Kyoto": {"iata": "KIX", "lat": 35.0116, "lon": 135.7681},
            "Marrakech": {"iata": "RAK", "lat": 31.6295, "lon": -7.9811},
            "Edinburgh": {"iata": "EDI", "lat": 55.9533, "lon": -3.1883},
            "Havana": {"iata": "HAV", "lat": 23.1136, "lon": -82.3666}
        }
        city_info = city_coordinates.get(request.location)
        if not city_info:
            raise HTTPException(status_code=400, detail="Unsupported location")

        pois = await fetch_pois(city_info["iata"])
        logging.info(f"Fetched POIs for {request.location}: {pois}")

        # Filter POIs based on updated interests
        user_vector = interests_to_vector(request.interests)
        logging.info(f"User interests vector: {user_vector}")

        filtered_pois = []
        similarity_threshold = 0.3
        for poi in pois:
            poi_interests = poi.get("interests", {})
            logging.info(f"POI {poi['name']} interests: {poi_interests}")
            poi_vector = interests_to_vector(poi_interests)
            logging.info(f"POI {poi['name']} vector: {poi_vector}")
            similarity = cosine_similarity([user_vector], [poi_vector])[0][0]
            logging.info(f"Similarity between user and POI {poi['name']}: {similarity}")
            if similarity >= similarity_threshold:
                poi["similarity"] = similarity
                filtered_pois.append(poi)

        filtered_pois.sort(key=lambda x: x["similarity"], reverse=True)
        logging.info(f"Filtered POIs: {filtered_pois}")

        if not filtered_pois:
            raise HTTPException(status_code=404, detail="No points of interest match your preferences")

        # Cluster POIs and assign to days
        daily_pois = cluster_pois(filtered_pois, days=request.days)
        logging.info(f"Daily POIs (names only for logging): {[[poi['name'] for poi in cluster] for cluster in daily_pois]}")
        logging.info(f"Daily POIs (full structure): {daily_pois}")

        # Generate updated plan
        plan_data = await generate_plan_with_gemini(
            request.location,
            request.start_date,
            request.days,
            request.interests,
            request.budget,
            daily_pois
        )

        # Update the plan in MongoDB
        updated_plan = {
            "location": request.location,
            "start_date": request.start_date,
            "days": request.days,
            "interests": request.interests,
            "budget": request.budget,
            "plan": plan_data["plan"],
            "hotel": plan_data["Hotel"]
        }
        db.plans.update_one({"_id": ObjectId(plan_id)}, {"$set": updated_plan})
        logging.info(f"Updated plan with plan_id: {plan_id}")

        return {"plan_id": plan_id, "plan": plan_data}
    except Exception as e:
        logging.error(f"Error in /edit-plan: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error editing plan: {str(e)}")  # Fixed syntax

@app.get("/hotels/search")
async def search_hotels(location: str, checkin: str, checkout: str):
    try:
        # Validate dates
        try:
            checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
            checkout_date = datetime.strptime(checkout, "%Y-%m-%d")
            if checkout_date <= checkin_date:
                raise ValueError("Checkout date must be after checkin date")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid date format or logic: {str(e)}")

        # Fetch mock hotels (replace with real API later)
        hotels = mock_hotels.get(location, [])
        if not hotels:
            raise HTTPException(status_code=404, detail="No hotels found for this location")

        return hotels
    except Exception as e:
        logging.error(f"Error in /hotels/search: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error searching hotels: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("shutdown")
def shutdown_event():
    mongo_client.close()
    logging.info("MongoDB Atlas connection closed")