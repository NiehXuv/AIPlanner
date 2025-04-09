# components/models.py
from pydantic import BaseModel, model_validator
from typing import Dict, List, Optional
from data.interests import interests

def validate_interests(data: dict, interests_field: str = "interests") -> dict:
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    interests_data = data.get(interests_field, {})
    if interests_data is not None:
        if not isinstance(interests_data, dict):
            raise ValueError("Interests must be a dictionary")
        valid_interests = set(interests)
        for interest in list(interests_data.keys()):
            if interest not in valid_interests:
                raise ValueError(f"Invalid interest: {interest}. Must be one of {valid_interests}")
            if interest == "ArtAndCulture":
                interests_data["Art & Culture"] = interests_data.pop(interest)
            score = interests_data[interest]
            if not (0 <= score <= 1):
                raise ValueError(f"Interest score for {interest} must be between 0 and 1, got {score}")
        data[interests_field] = interests_data
    return data

class PlanRequest(BaseModel):
    location: str
    start_date: str
    days: int
    interests: Dict[str, float]
    budget: float

    @model_validator(mode="before")
    @classmethod
    def check_interests(cls, data):
        return validate_interests(data)

class TimeSlot(BaseModel):
    time: Optional[str] = None
    activity: Optional[str] = None
    duration: Optional[str] = None

class DailyItinerary(BaseModel):
    day: int
    morning: Optional[TimeSlot] = None
    afternoon: Optional[TimeSlot] = None  # Updated to match the actual structure
    late_afternoon: Optional[TimeSlot] = None
    evening: Optional[TimeSlot] = None
    dinner: Optional[TimeSlot] = None
    night: Optional[TimeSlot] = None
    notes: Optional[str] = None

class EditPlanRequest(BaseModel):
    location: Optional[str] = None
    start_date: Optional[str] = None
    days: Optional[int] = None
    interests: Optional[Dict[str, float]] = None
    budget: Optional[float] = None
    plan: Optional[List[DailyItinerary]] = None
    hotel: Optional[Dict] = None

    @model_validator(mode="before")
    @classmethod
    def check_interests(cls, data):
        return validate_interests(data)