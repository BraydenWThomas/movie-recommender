import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.database import db
from app.secret_key_utils import get_secret_key

# Constants
SECRET_KEY = get_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI router
router = APIRouter()

# Pydantic models for request validation
class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Helper function to create a JWT token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Register a new user
@router.post("/register")
def create_user(user: UserCreateRequest):
    users_collection = db["users"]
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(user.password)
    new_user = {"email": user.email, "password": hashed_password, "recommendations": []}
    users_collection.insert_one(new_user)
    return {"message": "User registered successfully"}

# Login user
@router.post("/login")
def login_user(user: UserLoginRequest):
    users_collection = db["users"]
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Example protected route
@router.get("/protected")
def protected_route(token: str = Depends(create_access_token)):
    return {"message": "You have accessed a protected route"}
