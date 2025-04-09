# components/plan_generator.py
import google.generativeai as genai
import logging
import json
import re
import os
from datetime import datetime, timedelta
from amadeus import Client, ResponseError
from dotenv import load_dotenv
from datetime import datetime, timedelta
# Load environment variables
load_dotenv()

# Initialize Amadeus client
amadeus = Client(
    client_id=os.getenv("AMADEUS_API_KEY"),
    client_secret=os.getenv("AMADEUS_API_SECRET"),
    hostname="test"
)

async def generate_plan_with_gemini(location, start_date, days, interests, budget, daily_pois):
    try:
        # Calculate checkout date
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        checkout_date_obj = start_date_obj + timedelta(days=days)
        checkout_date = checkout_date_obj.strftime("%Y-%m-%d")

        # Validate start date is within 330 days from today
        today = datetime.now()
        max_start_date = today + timedelta(days=330)
        if start_date_obj > max_start_date:
            raise ValueError(f"Start date must be within 330 days from today ({max_start_date.strftime('%Y-%m-%d')})")

        # Get the city code (IATA code) for the location
        from data.cities import city_coordinates  # Import city_coordinates
        city_info = city_coordinates.get(location)
        if not city_info:
            raise ValueError("Unsupported location")

        city_code = city_info["iata"]
        if not city_code:
            raise ValueError("City code not found for this location")

        # Log the city code for debugging
        logging.info(f"Using cityCode: {city_code}")

        # Step 1: Use Hotel List API to get hotel IDs for the city
        try:
            hotel_list_response = amadeus.reference_data.locations.hotels.by_city.get(
                cityCode=city_code,
                ratings=["3", "4", "5"]  # Filter by ratings (list of strings)
            )
        except ResponseError as e:
            logging.error(f"Amadeus Hotel List API error: {str(e)}")
            logging.error(f"Error details: {e.response.body if e.response else 'No response body'}")
            hotel_recommendation = "Hotel recommendation unavailable"
        else:
            hotels_list = hotel_list_response.data
            if not hotels_list:
                hotel_recommendation = "No hotels found in Hotel List API"
            else:
                # Extract hotel IDs (limit to first 5 to avoid overwhelming the next API call)
                hotel_ids = [hotel["hotelId"] for hotel in hotels_list[:5]]
                # Store ratings from Hotel List API
                hotel_ratings_map = {hotel["hotelId"]: hotel.get("rating", 0) for hotel in hotels_list}
                logging.info(f"Retrieved hotel IDs: {hotel_ids}")

                # Step 2: Use Hotel Search API to get offers for the retrieved hotel IDs
                try:
                    response = amadeus.shopping.hotel_offers_search.get(
                        hotelIds=",".join(hotel_ids),  # Comma-separated string of hotel IDs
                        checkInDate=start_date,
                        checkOutDate=checkout_date,
                        adults=2,
                        currency="USD"
                    )
                except ResponseError as e:
                    logging.error(f"Amadeus Hotel Search API error: {str(e)}")
                    logging.error(f"Error details: {e.response.body if e.response else 'No response body'}")
                    hotel_recommendation = "Hotel recommendation unavailable"
                else:
                    hotels = response.data
                    if hotels:
                        top_hotel = hotels[0]
                        hotel_info = top_hotel.get("hotel", {})
                        hotel_id = hotel_info.get("hotelId")
                        offer = top_hotel.get("offers", [{}])[0]
                        price = offer.get("price", {}).get("total", "N/A")
                        # Use rating from Hotel List API
                        rating = hotel_ratings_map.get(hotel_id, 0)
                        hotel_recommendation = f"{hotel_info.get('name', 'Unknown Hotel')} (Rating: {rating}, Price: ${price})"
                    else:
                        hotel_recommendation = "No hotels found"

        # Prepare the prompt for Gemini
        prompt = f"""
        Generate a {days}-day travel itinerary for {location} starting on {start_date}.
        User interests: {interests}
        Budget: {budget}
        Points of Interest per day: {daily_pois}
        Include a hotel recommendation. I have already found a hotel: {hotel_recommendation}.
        Format the response as a JSON object with a "plan" array (one entry per day) and a "Hotel" field.
        Each day in the "plan" array should have a "day" field (as an integer, e.g., 1, 2, 3), "morning", "afternoon", "late_afternoon", "evening", "dinner", "night", and "notes" fields.
        Example:
        {{
            "plan": [
                {{"day": 1, "morning": {{"time": "9:00 AM", "activity": "Visit the Eiffel Tower", "duration": "2 hours"}}, "afternoon": {{"time": "12:00 PM", "activity": "Lunch", "duration": "1 hour"}}, "late_afternoon": {{}}, "evening": {{}}, "dinner": {{}}, "night": {{}}, "notes": ""}}
            ],
            "Hotel": "{hotel_recommendation}"
        }}
        """

        # Call Gemini API
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        plan_data = response.text  # Assume this is a JSON string

        # Log the raw response for debugging
        logging.info(f"Raw Gemini API response: {plan_data}")

        # Handle empty response
        if not plan_data or plan_data.strip() == "":
            raise ValueError("Gemini API returned an empty response")

        # Extract JSON from the response (in case it's embedded in extra text)
        json_match = re.search(r'\{.*\}', plan_data, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON object found in Gemini API response")

        json_str = json_match.group(0)
        logging.info(f"Extracted JSON string: {json_str}")

        # Parse the JSON response
        try:
            plan_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON: {str(e)}")
            raise ValueError(f"Gemini API response is not valid JSON: {json_str}")

        # Validate the response
        if "plan" not in plan_data or "Hotel" not in plan_data:
            raise ValueError("Invalid response format from Gemini API: missing 'plan' or 'Hotel' field")

        # Ensure the plan has the correct number of days
        if len(plan_data["plan"]) != days:
            raise ValueError(f"Expected {days} days in the plan, got {len(plan_data['plan'])}")

        # Fix the "day" field to ensure it's an integer
        for i, day_entry in enumerate(plan_data["plan"], start=1):
            if "day" not in day_entry:
                day_entry["day"] = i
            else:
                # Convert day to int and ensure it matches the expected day number
                try:
                    day_entry["day"] = int(day_entry["day"])
                except (ValueError, TypeError):
                    day_entry["day"] = i  # Fallback to the correct day number
                if day_entry["day"] != i:
                    logging.warning(f"Day {i} has incorrect day value {day_entry['day']}, correcting to {i}")
                    day_entry["day"] = i

        return plan_data
    except Exception as e:
        logging.error(f"Error generating plan with Gemini: {str(e)}")
        raise