from DataBase.habit import Period, Habit
from DataBase.habit_completion import HabitCompletion
from Services.auth import get_current_user
from Services.habit_management import list_habits


def run_analysis():
    menu_prompt = """
---Analysis---
    press 1 to list all tracked habits
    press 2 to list habits with a specific periodicity
    press 3 to get the longest run streak of all habits
    press 4 to get the longest run streak for a specific habit
    please enter your choice:
    """
    while (user_input := input(menu_prompt)) != "0":
        match user_input:
            case "1":
                list_habits()
            case "2":
                list_habits_with_same_periodicity()
            case "3":
                get_longest_run_streak_of_habits()

            case "4":
                get_longest_run_streak_of_habit()
def list_habits_with_same_periodicity():
    period_input = input("Enter periodicity (daily/weekly): ").strip().lower()
    period = Period(period_input)
    habits = []
    for habit in Habit.get_all_habits(get_current_user().id):
        if habit.period == period:
            habits.append(habit)
    if habits:
        print(f"Habits with periodicity {period.value}:")
        list_habits(habits)
        return habits
    else:
        print(f"No habits found with periodicity {period.value}.")
        return None

def get_longest_run_streak_of_habits():
    habits = Habit.get_all_habits(get_current_user().id)
    max_streak_per_habits = 0
    best_habit = None

    for habit in habits:
        completions = HabitCompletion.get(habit.id)
        periods = []
        for c in completions:
            periods.append(c.period_number)

        if len(periods) == 0:
            continue

        periods.sort()
        habit_maximum_streak = 0
        habit_streak = 1
        for i in range(1, len(periods)):
            if periods[i] == periods[i - 1] + 1:
                habit_streak += 1
            else:
                habit_streak = 1
            habit_maximum_streak = max(habit_maximum_streak, habit_streak)

        if max_streak_per_habits < habit_maximum_streak:
            best_habit = habit
            max_streak_per_habits = habit_maximum_streak

    if best_habit:
        print(f"Longest run streak: {max_streak_per_habits} periods for {best_habit}")
        return max_streak_per_habits
    else:
        print("No completed habits found.")
        return 0

def get_longest_run_streak_of_habit():
    list_habits()
    habit_id = input("Enter habit ID: ")

    completions = HabitCompletion.get(habit_id)
    periods = []
    for c in completions:
        periods.append(c.period_number)

    if len(periods) == 0:
        print("No completions found for this habit.")
        return 0;

    periods.sort()
    habit_maximum_streak = 0
    habit_streak = 1
    for i in range(1, len(periods)):
        if periods[i] == periods[i - 1] + 1:
            habit_streak += 1
        else:
            habit_streak = 1
        habit_maximum_streak = max(habit_maximum_streak, habit_streak)

    print(f"Longest run streak for {Habit.get(habit_id).title}: {habit_maximum_streak} periods")
    return habit_maximum_streak

