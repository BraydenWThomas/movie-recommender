from flask import Flask, request, jsonify
from pymongo import MongoClient
from models import create_user, verify_user

# Load configuration
from config import Config

app = Flask(__name__)

# MongoDB connection
client = MongoClient(Config.MONGO_URI)
db = client['movie_recommender']

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']
    create_user(email, password, db)
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    user = verify_user(email, password, db)
    if user:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/rate', methods=['POST'])
def rate_movie():
    data = request.json
    email = data['email']
    movie = data['movie']
    rating = data['rating']
    db['users'].update_one(
        {"email": email},
        {"$push": {"ratings": {"movie": movie, "rating": rating}}}
    )
    return jsonify({"message": "Rating added successfully"}), 201

@app.route('/ratings/<email>', methods=['GET'])
def get_ratings(email):
    user = db['users'].find_one({"email": email}, {"_id": 0, "ratings": 1})
    if user:
        return jsonify({"ratings": user['ratings']}), 200
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
