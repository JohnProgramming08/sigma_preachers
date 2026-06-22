import pytest
from sqlalchemy.exc import IntegrityError
from project.database import Insert

# Inserting a user
@pytest.mark.parametrize("username, password_hash", [
    ("Valid", 67),
    ("This is a super long password and stuff", 6785585686568),
    ("valid also", 1)
])
def test_insert_one_user_valid(app, username, password_hash):
    with app.app_context():
        assert Insert.insert_user(username, password_hash) == 1
    
def test_insert_many_users_valid(app):
    data = [
        ("Valid", 67),
        ("This is a super long password and stuff", 6785585686568),
        ("valid also", 1),
        ("also valid", 1)
    ]

    with app.app_context():
        for i, pair in enumerate(data):
            username = pair[0]
            password_hash = pair[1]
            assert Insert.insert_user(username, password_hash) == i + 1

@pytest.mark.parametrize("username, password_hash", [
    ("valid", "12"),
    ("valid", 32.0),
    ("valid", 32.2),
    ("valid", True), 
    ("valid", "just a string"),
    ("valid", "")
])
def test_insert_one_user_invalid(app, username, password_hash):
    with app.app_context():
        assert Insert.insert_user(username, password_hash) == -1

def test_insert_many_users_invalid(app):
    data = [
        ("valid", "12"),
        ("valid", 32.0),
        ("valid", 32.2),
        ("valid", True), 
        ("valid", "just a string"),
        ("valid", "")
    ]

    with app.app_context():
        for pair in data:
            username = pair[0]
            password_hash = pair[1]
            assert Insert.insert_user(username, password_hash) == -1

@pytest.mark.parametrize("username", [
    "Dylan", "James", "Wolfgang", "Max", "Dave", "This is a long a$$ name!"
])
def test_insert_user_erroneous(app, username):
    with app.app_context(), pytest.raises(IntegrityError):
        Insert.insert_user(username, 1)
        Insert.insert_user(username, 2)
    

