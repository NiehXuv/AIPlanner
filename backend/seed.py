# backend/seed.py
from pymongo import MongoClient
from data import pois

client = MongoClient("mongodb+srv://aiplanner:88PWRGXUCEX48HpF@aiplannercluster.j74dxd3.mongodb.net/?retryWrites=true&w=majority&appName=AIPlannerCluster")
db = client.trip_planner

db.pois.drop()
db.pois.insert_many(pois)
print("Seeded POIs successfully!")