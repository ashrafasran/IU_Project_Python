import pytest
from datetime import datetime
from DataBase.habit import Habit, Period
from DataBase.habit_completion import HabitCompletion
from DataBase.database import DATABASE

@pytest.fixture
def db():
    database = DATABASE()
    # Create the habits and habit_completions tables
    database.connection.execute(Habit.table(Habit))
    database.connection.execute(HabitCompletion.table(HabitCompletion))
    return database

@pytest.fixture
def habit(db):
    habit = Habit(user_id=1, title="Test Habit", description="Test Description", period=Period.DAILY)
    habit.save()
    return habit

@pytest.fixture
def habit_completion(habit):
    return HabitCompletion(habit=habit)

def test_save_completion(habit_completion):
    assert habit_completion.save() is True
    assert habit_completion.id is not None

def test_get_completions(habit_completion):
    habit_completion.save()
    completions = HabitCompletion.get(habit_completion.habit_id)
    assert len(completions) > 0
    assert completions[0].habit_id == habit_completion.habit_id

def test_calc_period_number(habit):
    completion_date = datetime.now()
    period_number = HabitCompletion.calc_period_number(habit, completion_date)
    assert period_number == (completion_date - habit.get_start_date()).days

def test_repr(habit_completion):
    habit_completion.save()
    repr_str = repr(habit_completion)
    assert repr_str == f"HabitCompletion( id={habit_completion.id}, habit_id={habit_completion.habit_id}, completion_date='{habit_completion.completion_date}', period_number={habit_completion.period_number} )"