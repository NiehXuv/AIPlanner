# backend/tag_pois_daily.py
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import pymongo
from data.interests import interests
from data.pois import hardcoded_pois
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)
logging.info(f"Loaded .env from: {env_path}")
logging.info(f"GEMINI_API_KEY from tag_pois_daily.py: {os.getenv('GEMINI_API_KEY')}")
logging.info(f"MONGO_URI from tag_pois_daily.py: {os.getenv('MONGO_URI')}")

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
    exit(1)

# Map IATA codes to city names
iata_to_city = {
    "PAR": "Paris",
    "TYO": "Tokyo",
    "BCN": "Barcelona",
    "NYC": "New York",
    "LON": "London",
    "ROM": "Rome",
    "SYD": "Sydney",
    "DXB": "Dubai",
    "SIN": "Singapore",
    "CPT": "Cape Town",
    "RIO": "Rio de Janeiro",
    "BKK": "Bangkok",
    "IST": "Istanbul",
    "SEL": "Seoul",
    "AMS": "Amsterdam",
    "PRG": "Prague",
    "VIE": "Vienna",
    "SFO": "San Francisco",
    "KIX": "Kyoto",
    "RAK": "Marrakech",
    "EDI": "Edinburgh",
    "HAV": "Havana"
}

def clean_gemini_response(response_text: str) -> str:
    """Clean Gemini response by removing Markdown code block formatting."""
    cleaned = response_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json"):].strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-len("```")].strip()
    return cleaned

def tag_pois_with_interests(pois: list, retries=3, delay=10, max_output_tokens=2000):
    batch_size = 5  # Process 5 POIs at a time to avoid truncation
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
                # Wait for the response to be fully generated
                time.sleep(delay)
                result = response.text
                logging.info(f"Gemini response for batch tagging (raw, batch {i//batch_size + 1}): {result}")
                
                cleaned_result = clean_gemini_response(result)
                logging.info(f"Gemini response for batch tagging (cleaned, batch {i//batch_size + 1}): {cleaned_result}")
                
                # Check if the response is a complete JSON array
                if not cleaned_result or not (cleaned_result.strip().startswith("[") and cleaned_result.strip().endswith("]")):
                    logging.warning(f"Incomplete Gemini response for batch {i//batch_size + 1}: {cleaned_result}")
                    raise ValueError("Gemini response is incomplete or not a JSON array")
                
                tagged_pois = json.loads(cleaned_result)
                # Verify the number of tagged POIs matches the batch size
                if len(tagged_pois) != len(batch):
                    logging.warning(f"Expected {len(batch)} POIs in response, but got {len(tagged_pois)}")
                    raise ValueError("Incomplete response: Number of tagged POIs does not match batch size")
                
                for tagged_poi in tagged_pois:
                    raw_interests = tagged_poi.get("interests", {})
                    normalized_interests = {}
                    for interest, score in raw_interests.items():
                        normalized_interest = interest.replace("ArtAndCulture", "Art & Culture")
                        if normalized_interest in interests:
                            normalized_interests[normalized_interest] = score
                    interests_dicts.append(normalized_interests)
                break  # Success, move to next batch
            except Exception as e:
                logging.error(f"Error batch tagging POIs (batch {i//batch_size + 1}, attempt {attempt + 1}/{retries}): {str(e)}")
                if attempt == retries - 1:
                    logging.warning(f"Max retries reached for batch {i//batch_size + 1}, falling back to individual tagging")
                    for poi in batch:
                        logging.info(f"Falling back to individual tagging for POI: {poi['name']}")
                        interests_dict = tag_poi_with_interests(poi["name"], poi["category"], retries=retries, delay=delay)
                        interests_dicts.append(interests_dict)
                        time.sleep(delay)
                else:
                    time.sleep(delay * (attempt + 1))  # Exponential backoff
    return interests_dicts

def tag_poi_with_interests(poi_name: str, category: str, retries=3, delay=10, max_output_tokens=200):
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
            
            interests_dict = json.loads(cleaned_result)
            normalized_interests = {}
            for interest, score in interests_dict.items():
                normalized_interest = interest.replace("ArtAndCulture", "Art & Culture")
                if normalized_interest in interests:
                    normalized_interests[normalized_interest] = score
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

def tag_and_store_all_pois():
    logging.info(f"Hardcoded POIs: {hardcoded_pois}")
    
    for city_iata, city_name in iata_to_city.items():
        logging.info(f"Tagging POIs for city IATA: {city_iata} (City: {city_name})")
        pois_data = hardcoded_pois.get(city_name, [])
        if not pois_data:
            logging.error(f"No POIs found for city {city_name} in hardcoded_pois")
            continue

        logging.info(f"POIs to tag for {city_name}: {pois_data}")
        pois_to_tag = [{"name": poi.get("name"), "category": poi.get("category", "SIGHTSEEING")} for poi in pois_data]
        interests_dicts = tag_pois_with_interests(pois_to_tag)

        formatted_pois = []
        for poi, interests_dict in zip(pois_data, interests_dicts):
            name = poi.get("name")
            formatted_pois.append({
                "city": city_iata,
                "name": name,
                "interests": interests_dict
            })
        logging.info(f"Tagged POIs for {city_name}: {formatted_pois}")

        if formatted_pois:
            try:
                db.pois.delete_many({"city": city_iata})
                db.pois.insert_many(formatted_pois)
                logging.info(f"Stored tagged POIs for {city_iata} in MongoDB Atlas")
            except Exception as e:
                logging.error(f"Error storing POIs for {city_iata} in MongoDB Atlas: {str(e)}")
        else:
            logging.warning(f"No POIs to store for {city_iata}")

if __name__ == "__main__":
    try:
        tag_and_store_all_pois()
    except Exception as e:
        logging.error(f"Error in tag_and_store_all_pois: {str(e)}")
    finally:
        mongo_client.close()
        logging.info("MongoDB Atlas connection closed")