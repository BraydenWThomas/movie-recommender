from fastapi import FastAPI
from app.routes import router

# Initialize FastAPI app
app = FastAPI(
    title="Movie Recommender API",
    description="API for managing users and movie recommendations.",
    version="1.0.0",
)

# Register routes
app.include_router(router)
