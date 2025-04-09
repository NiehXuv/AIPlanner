# backend/main.py
from fastapi import FastAPI, HTTPException
from components.models import PlanRequest, EditPlanRequest
from utils import fetch_pois
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pymongo
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
import logging
from bson.objectid import ObjectId
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import traceback
from amadeus import Client, ResponseError  # Import Amadeus SDK
from datetime import datetime, timedelta
# Import components
from components.vector import interests_to_vector
from components.plan_generator import generate_plan_with_gemini
from components.clustering import cluster_pois
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

# Initialize Amadeus client
amadeus = Client(
    client_id=os.getenv("AMADEUS_API_KEY"),
    client_secret=os.getenv("AMADEUS_API_SECRET"),
    hostname="test"
)

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

@app.get("/get-plan")
async def get_plan(plan_id: str):
    try:
        # Validate plan_id
        if not ObjectId.is_valid(plan_id):
            raise HTTPException(status_code=400, detail="Invalid plan_id")

        # Fetch the plan
        plan = db.plans.find_one({"_id": ObjectId(plan_id)})
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")

        return {
            "plan_id": plan_id,
            "location": plan["location"],
            "start_date": plan["start_date"],
            "days": plan["days"],
            "interests": plan["interests"],
            "budget": plan["budget"],
            "plan": {
                "plan": plan["plan"],
                "Hotel": plan["hotel"]
            }
        }
    except Exception as e:
        logging.error(f"Error in /get-plan: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error retrieving plan: {str(e)}")

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

            # Validate check-in date is within 330 days from today
            today = datetime.now()
            max_checkin_date = today + timedelta(days=330)
            if checkin_date > max_checkin_date:
                raise ValueError(f"Check-in date must be within 330 days from today ({max_checkin_date.strftime('%Y-%m-%d')})")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid date format or logic: {str(e)}")

        # Get the city code (IATA code) for the location
        city_info = city_coordinates.get(location)
        if not city_info:
            raise HTTPException(status_code=400, detail="Unsupported location")

        city_code = city_info["iata"]
        if not city_code:
            raise HTTPException(status_code=400, detail="City code not found for this location")

        # Log the city code for debugging
        logging.info(f"Using cityCode: {city_code}")

        # Step 1: Use Hotel List API to get hotel IDs for the city
        desired_hotel_count = 3  # We want exactly 3 hotels
        hotels_list = []

        # Fetch hotels from Hotel List API (without optional parameters for now)
        try:
            hotel_list_response = amadeus.reference_data.locations.hotels.by_city.get(
                cityCode=city_code
            )
        except ResponseError as e:
            logging.error(f"Amadeus Hotel List API error: {str(e)}")
            logging.error(f"Full error response: {e.response.body if e.response else 'No response body'}")
            raise HTTPException(status_code=500, detail=f"Hotel List API failed: {str(e)}")

        hotels_list = hotel_list_response.data
        if not hotels_list:
            raise HTTPException(status_code=404, detail="No hotels found for this location in Hotel List API")

        # Create a mapping of hotel IDs to their ratings
        hotel_ratings_map = {hotel["hotelId"]: hotel.get("rating", 0) for hotel in hotels_list}
        logging.info(f"Hotel ratings map: {hotel_ratings_map}")

        # Extract hotel IDs (limit to first 10 to match Amadeus API capability)
        hotel_ids = [hotel["hotelId"] for hotel in hotels_list[:10]]
        logging.info(f"Retrieved hotel IDs: {hotel_ids}")

        # Step 2: Use Hotel Search API to get offers for the retrieved hotel IDs
        formatted_hotels = []
        start_idx = 0
        batch_size = 10  # Maximum number of hotel IDs per API call

        while start_idx < len(hotel_ids) and len(formatted_hotels) < desired_hotel_count:
            # Take the next batch of hotel IDs
            batch_ids = hotel_ids[start_idx:start_idx + batch_size]
            if not batch_ids:
                break

            try:
                response = amadeus.shopping.hotel_offers_search.get(
                    hotelIds=",".join(batch_ids),
                    checkInDate=checkin,
                    checkOutDate=checkout,
                    adults=2,
                    currency="USD"
                )
                logging.info(f"Hotel Search API response: {response.data}")
            except ResponseError as e:
                logging.error(f"Amadeus Hotel Search API error: {str(e)}")
                logging.error(f"Error details: {e.response.body if e.response else 'No response body'}")
                start_idx += batch_size
                continue

            hotels = response.data
            if not hotels:
                start_idx += batch_size
                continue

            # Format the hotels from this batch
            for hotel in hotels:
                hotel_info = hotel.get("hotel", {})
                hotel_id = hotel_info.get("hotelId")
                offer = hotel.get("offers", [{}])[0]
                price = offer.get("price", {}).get("total", "N/A")
                rating = hotel_ratings_map.get(hotel_id, 0)

                # Convert price to a float for scoring (handle "N/A" case)
                price_value = float(price) if price != "N/A" else float("inf")

                # Calculate a match score: higher rating is better, lower price is better
                weight_rating = 100
                weight_price = 0.1
                score = (float(rating) * weight_rating) - (price_value * weight_price)

                formatted_hotels.append({
                    "name": hotel_info.get("name", "Unknown Hotel"),
                    "price": f"${price}" if price != "N/A" else "N/A",
                    "rating": rating,
                    "score": score
                })

                if len(formatted_hotels) >= desired_hotel_count:
                    break

            start_idx += batch_size

        if not formatted_hotels:
            raise HTTPException(status_code=404, detail="No hotels found for this location with available offers")

        # Sort hotels by score (descending) and take the top 3
        formatted_hotels.sort(key=lambda x: x["score"], reverse=True)
        top_hotels = formatted_hotels[:desired_hotel_count]

        # If fewer than 3 hotels are found, add mock hotels to reach 3
        if len(top_hotels) < desired_hotel_count:
            logging.warning(f"Only {len(top_hotels)} hotels found, adding mock data to reach {desired_hotel_count}")
            while len(top_hotels) < desired_hotel_count:
                top_hotels.append({
                    "name": f"Mock Hotel {len(top_hotels) + 1} in {location}",
                    "price": "$200.00",
                    "rating": "4"
                })

        # Remove the score field from the final response
        for hotel in top_hotels:
            if "score" in hotel:
                del hotel["score"]

        return top_hotels
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