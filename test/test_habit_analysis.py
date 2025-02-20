import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from DataBase.habit import Habit, Period
from DataBase.habit_completion import HabitCompletion
from DataBase.user import USER
from DataBase.database import DATABASE
from Services.analysis import list_habits_with_same_periodicity, get_longest_run_streak_of_habits, get_longest_run_streak_of_habit

# Fixture for database setup
@pytest.fixture
def db():
    database = DATABASE()
    database.connection.execute(USER.table(USER))
    database.connection.execute(Habit.table(Habit))
    database.connection.execute(HabitCompletion.table(HabitCompletion))
    return database

# Fixture for creating a user
@pytest.fixture
def user(db):
    # Use a unique email for each test to avoid conflicts
    email = f"test_{datetime.now().timestamp()}@example.com"
    user = USER(name="Test User", email=email, password="password")
    if not user.save():
        user = USER.get(email)
    return user

# Fixture for creating a habit
@pytest.fixture
def habit(user):
    habit = Habit(user_id=user.id, title="Test Habit", description="Test Description", period=Period.DAILY)
    habit.save()
    return habit

# Fixture for creating a habit completion
@pytest.fixture
def habit_completion(habit):
    completion = HabitCompletion(habit=habit, period_number=1)
    completion.save()
    return completion

# Test for listing habits by periodicity
@patch("Services.habit_management.list_habits")
@patch("builtins.input", return_value="daily")  # Mock input() to return "daily"
@patch("Services.analysis.get_current_user")  # Mock get_current_user() in the correct module
def test_list_habits_by_periodicity(mock_get_current_user, mock_input, mock_list_habits, user, habit):
    # Mock the current user
    mock_get_current_user.return_value = user

    # Debug: Print the mocked user
    print(f"Mocked User: {mock_get_current_user.return_value}")

    # Mock the list_habits function
    mock_list_habits.return_value = None

    # Mock the get_all_habits function
    with patch("DataBase.habit.Habit.get_all_habits", return_value=[habit]):
        habits = list_habits_with_same_periodicity()

    # Debug: Print the returned habits
    print(f"Returned Habits: {habits}")

    # Assertions
    assert habits is not None
    assert len(habits) == 1
    assert habits[0].period == Period.DAILY

# Test for getting the longest run streak of all habits
@patch("DataBase.habit.Habit.get_all_habits")
@patch("DataBase.habit_completion.HabitCompletion.get")
@patch("Services.analysis.get_current_user")  # Mock get_current_user() in the correct module
def test_longest_run_streak_all_habits(mock_get_current_user, mock_get_completions, mock_get_all_habits, user, habit, habit_completion):
    # Mock the current user
    mock_get_current_user.return_value = user

    # Debug: Print the mocked user
    print(f"Mocked User: {mock_get_current_user.return_value}")

    # Mock the get_all_habits function
    mock_get_all_habits.return_value = [habit]

    # Mock the get_completions function
    mock_get_completions.return_value = [habit_completion]

    # Call the function
    max_streak = get_longest_run_streak_of_habits()

    # Debug: Print the returned max streak
    print(f"Returned Max Streak: {max_streak}")

    # Assertions
    assert max_streak >= 0

# Test for getting the longest run streak of a specific habit
@patch("DataBase.habit.Habit.get")
@patch("DataBase.habit_completion.HabitCompletion.get")
@patch("Services.habit_management.get_current_user")  # Mock get_current_user() in the correct module
@patch("builtins.input", return_value="429")  # Mock input() to return the habit ID
def test_longest_run_streak_specific_habit(mock_input, mock_get_current_user, mock_get_completions, mock_get_habit, user, habit, habit_completion):
    # Mock the current user
    mock_get_current_user.return_value = user

    # Debug: Print the mocked user
    print(f"Mocked User: {mock_get_current_user.return_value}")

    # Mock the get_habit function
    mock_get_habit.return_value = habit

    # Mock the get_completions function
    mock_get_completions.return_value = [habit_completion]

    # Call the function
    longest_streak = get_longest_run_streak_of_habit()

    # Debug: Print the returned longest streak
    print(f"Returned Longest Streak: {longest_streak}")

    # Assertions
    assert longest_streak >= 0