# components/plan_generator.py
import google.generativeai as genai
import logging
import json
import re

async def generate_plan_with_gemini(location, start_date, days, interests, budget, daily_pois):
    try:
        # Prepare the prompt for Gemini
        prompt = f"""
        Generate a {days}-day travel itinerary for {location} starting on {start_date}.
        User interests: {interests}
        Budget: {budget}
        Points of Interest per day: {daily_pois}
        Include a hotel recommendation.
        Return ONLY a JSON object (no additional text) with a "plan" array (one entry per day) and a "Hotel" field.
        Each day in the "plan" array should have a "day" field (as an integer, e.g., 1, 2, 3), "morning", "afternoon", "late_afternoon", "evening", "dinner", "night", and "notes" fields.
        Example:
        {{
            "plan": [
                {{"day": 1, "morning": {{"time": "9:00 AM", "activity": "Visit the Eiffel Tower", "duration": "2 hours"}}, "afternoon": {{"lunch": {{}}}}, "late_afternoon": {{}}, "evening": {{}}, "dinner": {{}}, "night": {{}}, "notes": ""}}
            ],
            "Hotel": "Hotel Example"
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
        # Look for the first { and the last } to extract the JSON object
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