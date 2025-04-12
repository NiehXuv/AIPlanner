# backend/utils.py
import os
from openai import OpenAI
import google.generativeai as genai
from data.interests import interests
from data.cities import city_coordinates
from dotenv import load_dotenv
from pathlib import Path
import json
import pymongo
import logging
import time
import requests
from fastapi import HTTPException

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)
logging.info(f"Loaded .env from: {env_path}")
logging.info(f"OPENAI_API_KEY from utils.py: {os.getenv('OPENAI_API_KEY')}")
logging.info(f"GEMINI_API_KEY from utils.py: {os.getenv('GEMINI_API_KEY')}")
logging.info(f"MONGO_URI from utils.py: {os.getenv('MONGO_URI')}")
logging.info(f"HERE_API_KEY from utils.py: {os.getenv('HERE_API_KEY')}")

# Get HERE API key
HERE_API_KEY = os.getenv("HERE_API_KEY")
if not HERE_API_KEY:
    raise ValueError("HERE_API_KEY environment variable not set")

# Initialize OpenAI client (not used for now)
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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

# Map IATA codes to city names, derived from city_coordinates
iata_to_city = {info["iata"]: city for city, info in city_coordinates.items()}


def clean_gemini_response(response_text: str) -> str:
    """Clean Gemini response by removing Markdown code block formatting."""
    cleaned = response_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json"):].strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-len("```")].strip()
    return cleaned

async def fetch_city_coordinates(city_name: str):
    """Fetch city coordinates using HERE Geocoding API, with fallback to hardcoded data."""
    try:
        url = "https://geocode.search.hereapi.com/v1/geocode"
        params = {
            "q": city_name,
            "apiKey": HERE_API_KEY
        }
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to fetch city coordinates: {response.text}")
        
        data = response.json()
        if not data.get("items"):
            raise HTTPException(status_code=400, detail=f"City not found: {city_name}")
        
        position = data["items"][0]["position"]
        # Find the IATA code from iata_to_city
        iata = next((key for key, value in iata_to_city.items() if value.lower() == city_name.lower()), "UNKNOWN")
        return {
            "lat": position["lat"],
            "lon": position["lng"],
            "iata": iata
        }
    except Exception as e:
        logging.warning(f"Failed to fetch city coordinates from HERE API: {str(e)}. Falling back to hardcoded data.")
        # Fallback to hardcoded data
        city_info = next((info for city, info in city_coordinates.items() if city.lower() == city_name.lower()), None)
        if not city_info:
            raise HTTPException(status_code=400, detail=f"Unsupported location: {city_name}")
        return city_info

async def fetch_pois(city_iata: str):
    """Fetch POIs for a city using HERE API, tag them with interests, and cache in MongoDB."""
    logging.info(f"Fetching POIs for city IATA: {city_iata} from MongoDB Atlas")
    pois = list(db.pois.find({"city": city_iata}))
    if pois:
        # Remove duplicates based on POI name
        seen_names = set()
        unique_pois = []
        for poi in pois:
            if poi["name"] not in seen_names:
                seen_names.add(poi["name"])
                unique_pois.append(poi)
            else:
                logging.warning(f"Duplicate POI found in database for {city_iata}: {poi['name']}")
        logging.info(f"Found POIs in MongoDB Atlas for {city_iata} (after deduplication): {unique_pois}")
        return unique_pois

    logging.info(f"No POIs found in MongoDB Atlas for {city_iata}, fetching from HERE API")
    city_name = iata_to_city.get(city_iata)
    if not city_name:
        logging.error(f"No city name found for IATA code {city_iata}")
        return []

    # Fetch city coordinates
    city_info = await fetch_city_coordinates(city_name)
    lat, lon = city_info["lat"], city_info["lon"]

    # Fetch POIs using HERE API
    url = "https://discover.search.hereapi.com/v1/discover"
    params = {
        "q": f"tourist attractions in {city_name}",
        "at": f"{lat},{lon}",
        "limit": 20,  # HERE API limits to 20 results per request
        "apiKey": HERE_API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to fetch POIs from HERE API: {response.text}")
    
    data = response.json()
    if not data.get("items"):
        logging.warning(f"No POIs found for {city_name} using HERE API")
        return []

    # Process HERE API results
    pois_data = []
    for item in data["items"]:
        # Map HERE categories to a simplified category for tagging
        categories = [cat["id"] for cat in item.get("categories", [])]
        category = "SIGHTSEEING"  # Default category
        if "museum" in categories:
            category = "MUSEUM"
        elif "park" in categories:
            category = "PARK"
        elif "beach" in categories:
            category = "BEACH"
        elif "monument" in categories:
            category = "MONUMENT"
        elif "landmark" in categories:
            category = "LANDMARK"
        
        poi = {
            "name": item["title"],
            "category": category,
            "lat": item["position"]["lat"],
            "lon": item["position"]["lng"]
        }
        pois_data.append(poi)

    # Remove duplicates from fetched POIs
    seen_names = set()
    unique_pois_data = []
    for poi in pois_data:
        if poi["name"] not in seen_names:
            seen_names.add(poi["name"])
            unique_pois_data.append(poi)
        else:
            logging.warning(f"Duplicate POI found in HERE API response for {city_name}: {poi['name']}")
    pois_data = unique_pois_data

    logging.info(f"POIs fetched from HERE API for {city_name} (after deduplication): {pois_data}")
    if not pois_data:
        logging.error(f"No POIs found for city {city_name} after deduplication")
        return []

    # Tag POIs with interests using Gemini
    pois_to_tag = [{"name": poi["name"], "category": poi["category"]} for poi in pois_data]
    interests_dicts = await tag_pois_with_interests(pois_to_tag)

    if not interests_dicts:
        logging.error(f"Failed to tag POIs for {city_name}. Using fallback interests.")
        interests_dicts = []
        for poi in pois_data:
            category = poi.get("category", "SIGHTSEEING")
            fallback_mapping = {
                "SIGHTSEEING": {"Historical": 0.8, "Art & Culture": 0.6},
                "MUSEUM": {"Historical": 0.8, "Art & Culture": 0.8},
                "PARK": {"Nature": 0.8, "Relaxing": 0.6},
                "SHOPPING": {"Shopping": 0.8},
                "ENTERTAINMENT": {"Entertainment": 0.8},
                "BEACH": {"Nature": 0.8, "Relaxing": 0.7},
                "SPORT": {"Sports": 0.8},
                "ADVENTURE": {"Adventure": 0.8},
                "HISTORIC": {"Historical": 0.9, "Art & Culture": 0.5},
                "LANDMARK": {"Historical": 0.8, "Art & Culture": 0.6},
                "MONUMENT": {"Historical": 0.9, "Art & Culture": 0.4}
            }
            fallback_interests = fallback_mapping.get(category, {"Entertainment": 0.5})
            interests_dicts.append(fallback_interests)

    # Format POIs for storage
    formatted_pois = []
    for poi, interests_dict in zip(pois_data, interests_dicts):
        formatted_poi = {
            "city": city_iata,
            "name": poi["name"],
            "interests": interests_dict,
            "lat": poi["lat"],
            "lon": poi["lon"]
        }
        formatted_pois.append(formatted_poi)
    logging.info(f"Formatted POIs for {city_iata}: {formatted_pois}")

    # Store in MongoDB
    if formatted_pois:
        try:
            db.pois.insert_many(formatted_pois)
            logging.info(f"Stored tagged POIs for {city_iata} in MongoDB Atlas")
        except Exception as e:
            logging.error(f"Error storing POIs for {city_iata} in MongoDB Atlas: {str(e)}")

    return formatted_pois

async def tag_pois_with_interests(pois: list, retries=3, delay=5, max_output_tokens=4000):
    batch_size = 10
    interests_dicts = []
    
    for i in range(0, len(pois), batch_size):
        batch = pois[i:i + batch_size]
        logging.info(f"Processing batch {i//batch_size + 1} with {len(batch)} POIs")
        
        for attempt in range(retries):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = (
                    "Classify the following points of interest into one or more of these interests: "
                    f"{', '.join(interests)}. Assign a score between 0 and 1 for each interest based on relevance. "
                    "Return the result as a JSON array where each element is an object with 'name', 'category', and 'interests' (a dictionary of interest names and scores).\n"
                )
                for poi in batch:
                    prompt += f"- Name: {poi['name']}, Category: {poi['category']}\n"
                
                logging.info(f"Gemini prompt for batch tagging (batch {i//batch_size + 1}): {prompt}")
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": max_output_tokens,
                        "temperature": 0.5
                    }
                )
                time.sleep(delay)
                result = response.text
                logging.info(f"Gemini response for batch tagging (raw, batch {i//batch_size + 1}): {result}")
                
                cleaned_result = clean_gemini_response(result)
                logging.info(f"Gemini response for batch tagging (cleaned, batch {i//batch_size + 1}): {cleaned_result}")
                
                if not cleaned_result or not (cleaned_result.strip().startswith("[") and cleaned_result.strip().endswith("]")):
                    logging.warning(f"Incomplete Gemini response for batch {i//batch_size + 1}: {cleaned_result}")
                    raise ValueError("Gemini response is incomplete or not a JSON array")
                
                try:
                    tagged_pois = json.loads(cleaned_result)
                except json.JSONDecodeError as e:
                    logging.error(f"Failed to parse Gemini response as JSON (batch {i//batch_size + 1}): {cleaned_result}")
                    raise ValueError(f"Invalid JSON response from Gemini: {str(e)}")
                
                if len(tagged_pois) != len(batch):
                    logging.warning(f"Expected {len(batch)} POIs in response, but got {len(tagged_pois)}: {tagged_pois}")
                    raise ValueError("Incomplete response: Number of tagged POIs does not match batch size")
                
                for tagged_poi in tagged_pois:
                    if "name" not in tagged_poi or "category" not in tagged_poi or "interests" not in tagged_poi:
                        logging.error(f"Invalid tagged POI in batch {i//batch_size + 1}: {tagged_poi}")
                        raise ValueError("Tagged POI missing required fields")
                    
                    raw_interests = tagged_poi.get("interests", {})
                    normalized_interests = {}
                    for interest, score in raw_interests.items():
                        normalized_interest = interest.replace("ArtAndCulture", "Art & Culture")
                        if normalized_interest in interests:
                            normalized_interests[normalized_interest] = max(0.0, min(1.0, float(score)))
                    interests_dicts.append(normalized_interests)
                break
            except Exception as e:
                logging.error(f"Error batch tagging POIs (batch {i//batch_size + 1}, attempt {attempt + 1}/{retries}): {str(e)}")
                if attempt == retries - 1:
                    logging.warning(f"Max retries reached for batch {i//batch_size + 1}, falling back to individual tagging")
                    for poi in batch:
                        logging.info(f"Falling back to individual tagging for POI: {poi['name']}")
                        interests_dict = await tag_poi_with_interests(poi["name"], poi["category"], retries=retries, delay=delay)
                        interests_dicts.append(interests_dict)
                        time.sleep(delay)
                else:
                    time.sleep(delay * (attempt + 1))
    return interests_dicts

async def tag_poi_with_interests(poi_name: str, category: str, retries=3, delay=15, max_output_tokens=400):
    for attempt in range(retries):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = (
                f"Given the point of interest '{poi_name}' with category '{category}', classify it into one or more of these interests: "
                f"{', '.join(interests)}. Assign a score between 0 and 1 for each interest based on relevance. "
                f"Return the result as a JSON object with interest names as keys and scores as values."
            )
            logging.info(f"Gemini prompt for individual tagging of '{poi_name}': {prompt}")
            response = model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": max_output_tokens,
                    "temperature": 0.5
                }
            )
            time.sleep(delay)
            result = response.text
            logging.info(f"Gemini response for individual tagging of '{poi_name}' (raw): {result}")
            
            cleaned_result = clean_gemini_response(result)
            logging.info(f"Gemini response for individual tagging of '{poi_name}' (cleaned): {cleaned_result}")
            
            if not cleaned_result or not (cleaned_result.strip().startswith("{") and cleaned_result.strip().endswith("}")):
                logging.warning(f"Incomplete Gemini response for '{poi_name}': {cleaned_result}")
                raise ValueError("Gemini response is incomplete or not a JSON object")
            
            try:
                interests_dict = json.loads(cleaned_result)
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse Gemini response as JSON for '{poi_name}': {cleaned_result}")
                raise ValueError(f"Invalid JSON response from Gemini: {str(e)}")
            
            normalized_interests = {}
            for interest, score in interests_dict.items():
                normalized_interest = interest.replace("ArtAndCulture", "Art & Culture")
                if normalized_interest in interests:
                    normalized_interests[normalized_interest] = max(0.0, min(1.0, float(score)))
            return normalized_interests
        except Exception as e:
            logging.error(f"Error tagging POI '{poi_name}' with Gemini (attempt {attempt + 1}/{retries}): {str(e)}")
            if attempt == retries - 1:
                logging.warning(f"Max retries reached for POI '{poi_name}', using fallback")
                fallback_mapping = {
                    "SIGHTSEEING": {"Historical": 0.8, "Art & Culture": 0.6},
                    "MUSEUM": {"Historical": 0.8, "Art & Culture": 0.8},
                    "PARK": {"Nature": 0.8, "Relaxing": 0.6},
                    "SHOPPING": {"Shopping": 0.8},
                    "ENTERTAINMENT": {"Entertainment": 0.8},
                    "BEACH": {"Nature": 0.8, "Relaxing": 0.7},
                    "SPORT": {"Sports": 0.8},
                    "ADVENTURE": {"Adventure": 0.8},
                    "HISTORIC": {"Historical": 0.9, "Art & Culture": 0.5},
                    "LANDMARK": {"Historical": 0.8, "Art & Culture": 0.6},
                    "MONUMENT": {"Historical": 0.9, "Art & Culture": 0.4}
                }
                fallback_interests = fallback_mapping.get(category, {"Entertainment": 0.5})
                logging.info(f"Fallback interests for POI '{poi_name}' (category: {category}): {fallback_interests}")
                return fallback_interests
            time.sleep(delay * (attempt + 1))