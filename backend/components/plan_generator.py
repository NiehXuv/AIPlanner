# components/plan_generator.py
import google.generativeai as genai
import logging
from datetime import datetime, timedelta
import json
from components.response import clean_gemini_response
async def generate_plan_with_gemini(location, start_date, days, interests, budget, daily_pois):
    """
    Generate a travel plan using Gemini API, ensuring a unique plan for each day.
    
    Args:
        location (str): The city for the trip.
        start_date (str): Start date of the trip in YYYY-MM-DD format.
        days (int): Number of days for the trip.
        interests (dict): User's interests with weights.
        budget (float): User's budget in USD.
        daily_pois (list): List of lists, where each inner list contains POIs for a day.
    
    Returns:
        dict: A dictionary containing the plan and hotel suggestion.
    """
    logging.info(f"Generating plan for {location} starting on {start_date} for {days} days")
    
    # Convert start_date to datetime object
    start = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Prepare the prompt for Gemini
    interests_str = ", ".join([f"{k} ({v})" for k, v in interests.items()])
    prompt = (
        f"Create a detailed travel itinerary for a {days}-day trip to {location}, starting on {start_date}. "
        f"The traveler's interests are: {interests_str}. Their budget is ${budget} USD for the entire trip. "
        f"Below are the points of interest (POIs) assigned to each day based on geographical proximity. "
        f"You must use ONLY the POIs assigned to each day for that day's itinerary, ensuring no overlap of POIs across days:\n"
    )
    
    # Add daily POIs to the prompt
    for day in range(days):
        date = (start + timedelta(days=day)).strftime("%Y-%m-%d")
        poi_names = [poi["name"] for poi in daily_pois[day]]
        prompt += f"\nDay {day + 1} ({date}): {', '.join(poi_names) if poi_names else 'No POIs assigned'}"
    
    prompt += (
        "\n\nFor each day, provide a detailed itinerary including:\n"
        "- Morning, afternoon, and evening activities based on the assigned POIs for that day.\n"
        "- Suggested times for each activity.\n"
        "- Recommendations for meals (breakfast, lunch, dinner) with budget-friendly options.\n"
        "- Any additional activities or tips relevant to the traveler's interests, but do not include POIs from other days.\n"
        "At the end, suggest a budget-friendly hotel in {location} that aligns with the traveler's interests and budget.\n"
        "Format the response as a JSON object with a 'plan' key containing a list of daily itineraries and a 'Hotel' key with the hotel suggestion."
    )
    
    logging.info(f"Prompt for Gemini: {prompt}")
    
    # Call Gemini API
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        response_text = response.text
        logging.info(f"Raw response from Gemini: {response_text}")
        
        # Clean and parse the response
        cleaned_response = clean_gemini_response(response_text)
        plan_data = json.loads(cleaned_response)
        
        # Validate the response structure
        if "plan" not in plan_data or "Hotel" not in plan_data:
            logging.error("Invalid response structure from Gemini")
            raise ValueError("Invalid response structure from Gemini")
        
        # Validate that each day's itinerary only uses the assigned POIs
        for day in range(days):
            assigned_poi_names = set(poi["name"] for poi in daily_pois[day])
            other_days_poi_names = set(
                poi["name"] for d in range(days) if d != day for poi in daily_pois[d]
            )
            
            # Extract POIs mentioned in the day's itinerary
            day_plan = plan_data["plan"][day]
            itinerary_text = json.dumps(day_plan).lower()
            for poi_name in other_days_poi_names:
                if poi_name.lower() in itinerary_text:
                    logging.error(f"Day {day + 1} itinerary includes POI '{poi_name}' which is assigned to another day")
                    raise ValueError(f"Day {day + 1} itinerary includes POI '{poi_name}' which is assigned to another day")
            
            # Ensure at least one assigned POI is mentioned (if there are any)
            if assigned_poi_names:
                mentioned = False
                for poi_name in assigned_poi_names:
                    if poi_name.lower() in itinerary_text:
                        mentioned = True
                        break
                if not mentioned:
                    logging.warning(f"Day {day + 1} itinerary does not mention any of the assigned POIs: {assigned_poi_names}")
        
        return plan_data
    except Exception as e:
        logging.error(f"Error generating plan with Gemini: {str(e)}")
        raise