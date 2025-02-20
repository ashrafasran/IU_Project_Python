import pytest
from DataBase.habit import Habit, Period
from DataBase.database import DATABASE

@pytest.fixture
def db():
    database = DATABASE()
    database.connection.execute(Habit.table(Habit))
    return database

@pytest.fixture
def habit(db):
    return Habit(user_id=1, title="Test Habit", description="Test Description", period=Period.DAILY)

def test_save_habit(habit):
    assert habit.save() is True
    assert habit.id is not None

def test_update_habit(habit):
    habit.save()
    habit.update(title="Updated Title")
    updated_habit = Habit.get(habit.id)
    assert updated_habit.title == "Updated Title"

def test_delete_habit(habit):
    habit.save()
    assert Habit.delete(habit.id) is True
    assert Habit.get(habit.id) is None