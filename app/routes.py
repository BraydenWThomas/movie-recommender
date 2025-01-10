from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import db

router = APIRouter()


# Define Pydantic models for request bodies
class UserRegisterRequest(BaseModel):
    email: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class RecommendationRequest(BaseModel):
    movie: str
    rating: float


# Test endpoint
@router.get("/")
def read_root():
    return {"message": "Welcome to the Movie Recommender API"}


# Register a new user
@router.post("/register")
def create_user(request: UserRegisterRequest):
    users_collection = db["users"]
    if users_collection.find_one({"email": request.email}):
        raise HTTPException(status_code=400, detail="User already exists")
    user_data = {"email": request.email, "password": request.password, "recommendations": []}
    users_collection.insert_one(user_data)
    return {"message": "User registered successfully"}


# Login user
@router.post("/login")
def login_user(request: UserLoginRequest):
    users_collection = db["users"]
    user = users_collection.find_one({"email": request.email, "password": request.password})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}


# Add a recommendation
@router.post("/recommendations/{email}")
def add_recommendation(email: str, request: RecommendationRequest):
    users_collection = db["users"]
    result = users_collection.update_one(
        {"email": email},
        {"$push": {"recommendations": {"movie": request.movie, "rating": request.rating}}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Recommendation added successfully"}


# Get user recommendations
@router.get("/recommendations/{email}")
def get_recommendations(email: str):
    users_collection = db["users"]
    user = users_collection.find_one({"email": email}, {"_id": 0, "recommendations": 1})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"recommendations": user.get("recommendations", [])}
