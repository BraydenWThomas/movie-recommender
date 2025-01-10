from pymongo import MongoClient
from app.settings import settings

# MongoDB client and database
client = MongoClient(settings.MONGO_URI)
db = client["movie_recommender"]
