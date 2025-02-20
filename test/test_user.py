import pytest
from DataBase.user import USER
from DataBase.database import DATABASE


@pytest.fixture
def setup_database():
    """Fixture to reset the database before each test."""
    db = DATABASE()
    cursor = db.connect().cursor()

    # Ensure table exists
    cursor.execute(USER().table())

    # Clear previous test data
    cursor.execute("DELETE FROM users")
    db.connect().commit()

    return db


@pytest.fixture
def user(setup_database):
    """Fixture to create a user instance without saving it."""
    return USER(name="Test User", email="test@example.com", password="password123")


def test_save_user(user):
    """Test saving a new user."""
    print(f"Testing save user: {user}")
    assert user.save() is True, "User save failed, email might already exist."
