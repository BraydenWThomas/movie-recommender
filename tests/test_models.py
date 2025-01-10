from models import create_user, verify_user

def test_create_user(db_mock):
    create_user("test@example.com", "password123", db_mock)
    assert db_mock['users'].find_one({"email": "test@example.com"}) is not None

def test_verify_user(db_mock):
    create_user("test@example.com", "password123", db_mock)
    assert verify_user("test@example.com", "password123", db_mock) is not None
