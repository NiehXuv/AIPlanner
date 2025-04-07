# backend/data.py
cities = [
    {"name": "Abu Dhabi", "country": "United Arab Emirates", "iata": "AUH"},
    {"name": "Amsterdam", "country": "The Netherlands", "iata": "AMS"},
    {"name": "Ankara", "country": "Turkey", "iata": "ANK"},
    {"name": "Antalya", "country": "Turkey", "iata": "AYT"},
    {"name": "Athens", "country": "Greece", "iata": "ATH"},
    {"name": "Baku", "country": "Azerbaijan", "iata": "GYD"},
    {"name": "Bangkok", "country": "Thailand", "iata": "BKK"},
    {"name": "Barcelona", "country": "Spain", "iata": "BCN"},
    {"name": "Berlin", "country": "Germany", "iata": "BER"},
    {"name": "Brussels", "country": "Belgium", "iata": "BRU"},
    {"name": "Hanoi", "country": "Vietnam", "iata": "HAN"},
    {"name": "Paris", "country": "France", "iata": "PAR"},
    {"name": "Tokyo", "country": "Japan", "iata": "TYO"}
]

interests = [
    "Historical",
    "Art & Culture",
    "Nature",
    "Entertainment",
    "Shopping",
    "Sports",
    "Adventure",
    "Relaxing"
]

pois = [
    {"city": "HAN", "name": "Temple of Literature", "interests": {"Historical": 0.9, "Art & Culture": 0.7}},
    {"city": "HAN", "name": "Old Quarter", "interests": {"Food": 0.8, "Shopping": 0.6}},
    {"city": "PAR", "name": "Louvre", "interests": {"Art & Culture": 0.9, "Historical": 0.7}},
    {"city": "BKK", "name": "Grand Palace", "interests": {"Historical": 0.8, "Art & Culture": 0.6}},
]