from werkzeug.security import generate_password_hash, check_password_hash

def create_user(email, password, db):
    users = db['users']
    hashed_password = generate_password_hash(password)
    user = {"email": email, "password": hashed_password, "ratings": []}
    users.insert_one(user)

def verify_user(email, password, db):
    users = db['users']
    user = users.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        return user
    return None
