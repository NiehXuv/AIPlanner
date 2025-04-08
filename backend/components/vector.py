# backend/components/vector.py
import numpy as np
from data.interests import interests

def interests_to_vector(interests_dict: dict, all_interests: list = interests) -> np.ndarray:
    vector = np.zeros(len(all_interests))
    for interest, score in interests_dict.items():
        if interest in all_interests:
            idx = all_interests.index(interest)
            vector[idx] = score
    return vector