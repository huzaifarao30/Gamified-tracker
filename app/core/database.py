import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
    print("Successfully connected to database")
except Exception as e:
    print(f"Failed to connect to database : {e}")

db = client.habit_rpg
task_collection = db.tasks
character_collection = db.characters