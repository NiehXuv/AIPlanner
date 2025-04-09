# backend/main.py
from fastapi import FastAPI, HTTPException
from components.models import PlanRequest, EditPlanRequest
from utils import fetch_pois
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pymongo
from pymongo.read_concern import ReadConcern  # Import ReadConcern
from pymongo.write_concern import WriteConcern  # Import WriteConcern
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
from data.cities import city_coordinates

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

# Set write_concern and read_concern for the plans collection
db.plans = db["plans"].with_options(
    write_concern=WriteConcern(w="majority"),
    read_concern=ReadConcern("majority")
)

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

# Endpoints
@app.post("/generate-plan")
async def generate_plan(request: PlanRequest):
    try:
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
        try:
            plan_data = await generate_plan_with_gemini(
                request.location,
                request.start_date,
                request.days,
                request.interests,
                request.budget,
                daily_pois
            )
        except ValueError as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")

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
async def edit_plan(plan_id: str, request: EditPlanRequest):
    try:
        # Validate plan_id
        if not ObjectId.is_valid(plan_id):
            raise HTTPException(status_code=400, detail="Invalid plan_id")

        # Fetch the existing plan
        plan = db.plans.find_one({"_id": ObjectId(plan_id)})
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")

        # Log the original plan
        logging.info(f"Original plan: {plan}")

        # Prepare the update dictionary
        update_data = {}

        # Validate and update location (cannot be changed)
        if request.location is not None:
            if request.location != plan["location"]:
                raise HTTPException(status_code=400, detail="Location cannot be changed")
            update_data["location"] = request.location

        # Update other top-level fields if provided
        if request.start_date is not None:
            update_data["start_date"] = request.start_date
        if request.days is not None:
            update_data["days"] = request.days
            # If plan["plan"] exists, truncate or pad it to match the new number of days
            if "plan" in plan:
                current_plan = plan["plan"]
                # Convert day to int to handle string values
                existing_daily_plans = {int(day["day"]) if isinstance(day["day"], str) else day["day"]: day for day in current_plan}
                new_plan = []
                for day_num in range(1, request.days + 1):
                    if day_num in existing_daily_plans:
                        day_entry = existing_daily_plans[day_num]
                        # Ensure day is an int in the updated plan
                        day_entry["day"] = int(day_entry["day"])
                        new_plan.append(day_entry)
                    else:
                        new_plan.append({
                            "day": day_num,
                            "morning": {},
                            "afternoon": {},
                            "late_afternoon": {},
                            "evening": {},
                            "dinner": {},
                            "night": {},
                            "notes": ""
                        })
                update_data["plan"] = new_plan
        if request.interests is not None:
            update_data["interests"] = request.interests
        if request.budget is not None:
            update_data["budget"] = request.budget
        if request.hotel is not None:
            update_data["hotel"] = request.hotel

        # Update specific days in the plan if provided
        if request.plan is not None:
            # Convert existing plan["plan"] to a dictionary for easier merging
            # Handle string day values by converting to int
            existing_daily_plans = {int(day["day"]) if isinstance(day["day"], str) else day["day"]: day for day in plan["plan"]}
            
            # Merge updates from the request
            for updated_day in request.plan:
                day_num = updated_day.day
                if day_num < 1 or day_num > plan["days"]:
                    raise HTTPException(status_code=400, detail=f"Invalid day number: {day_num}. Must be between 1 and {plan['days']}")
                
                # Get the existing day or create a new one
                if day_num in existing_daily_plans:
                    existing_day = existing_daily_plans[day_num]
                else:
                    existing_day = {
                        "day": day_num,
                        "morning": {},
                        "afternoon": {},
                        "late_afternoon": {},
                        "evening": {},
                        "dinner": {},
                        "night": {},
                        "notes": ""
                    }

                # Update fields if provided
                if updated_day.morning is not None:
                    existing_day["morning"] = updated_day.morning.dict(exclude_unset=True)
                if updated_day.afternoon is not None:
                    existing_day["afternoon"] = updated_day.afternoon.dict(exclude_unset=True)
                if updated_day.late_afternoon is not None:
                    existing_day["late_afternoon"] = updated_day.late_afternoon.dict(exclude_unset=True)
                if updated_day.evening is not None:
                    existing_day["evening"] = updated_day.evening.dict(exclude_unset=True)
                if updated_day.dinner is not None:
                    existing_day["dinner"] = updated_day.dinner.dict(exclude_unset=True)
                if updated_day.night is not None:
                    existing_day["night"] = updated_day.night.dict(exclude_unset=True)
                if updated_day.notes is not None:
                    existing_day["notes"] = updated_day.notes
                
                # Ensure day is an int
                existing_day["day"] = int(day_num)
                existing_daily_plans[day_num] = existing_day

            # Convert back to a list and sort by day
            updated_plan_list = sorted(existing_daily_plans.values(), key=lambda x: x["day"])
            update_data["plan"] = updated_plan_list

        # Log the update data
        logging.info(f"Update data: {update_data}")

        # If no fields were updated, return the original plan
        if not update_data:
            logging.info("No fields to update, returning original plan")
            return {"plan_id": plan_id, "plan": {"plan": plan["plan"], "Hotel": plan["hotel"]}}

        # Update the plan in MongoDB
        result = db.plans.update_one(
            {"_id": ObjectId(plan_id)},
            {"$set": update_data}
        )
        logging.info(f"Updated plan with plan_id: {plan_id}, matched: {result.matched_count}, modified: {result.modified_count}")

        # Fetch the updated plan
        updated_plan = db.plans.find_one({"_id": ObjectId(plan_id)})
        logging.info(f"Updated plan from DB: {updated_plan}")

        return {
            "plan_id": plan_id,
            "plan": {
                "plan": updated_plan["plan"],
                "Hotel": updated_plan["hotel"]
            }
        }
    except Exception as e:
        logging.error(f"Error in /edit-plan: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error editing plan: {str(e)}")

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