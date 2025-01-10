from fastapi import FastAPI
from database import db

app = FastAPI()

# Test endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Recommender API"}

# Create a test user
@app.post("/users")
def create_user(username: str, email: str):
    users_collection = db["users"]
    user = {"username": username, "email": email, "recommendations": []}
    result = users_collection.insert_one(user)
    return {"message": "User created", "user_id": str(result.inserted_id)}

# Get all users
@app.get("/users")
def get_users():
    users_collection = db["users"]
    users = list(users_collection.find({}, {"_id": 0}))
    return {"users": users}

# Add a recommendation for a user
@app.post("/recommendations/{user_id}")
def add_recommendation(user_id: str, item_id: str, rating: float):
    users_collection = db["users"]
    result = users_collection.update_one(
        {"_id": user_id},
        {"$push": {"recommendations": {"item_id": item_id, "rating": rating}}}
    )
    if result.matched_count == 0:
        return {"error": "User not found"}
    return {"message": "Recommendation added"}

# Get recommendations for a user
@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: str):
    users_collection = db["users"]
    user = users_collection.find_one({"_id": user_id}, {"recommendations": 1})
    if not user:
        return {"error": "User not found"}
    return {"recommendations": user.get("recommendations", [])}
