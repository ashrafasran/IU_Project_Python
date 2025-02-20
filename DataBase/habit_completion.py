from datetime import datetime
from DataBase.database import DATABASE
from DataBase.habit import Habit, Period


class HabitCompletion:
    db = DATABASE()

    def table(self):
        return """
            CREATE TABLE IF NOT EXISTS habit_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completion_date DATETIME NOT NULL,
                period_number INTEGER NOT NULL,
                FOREIGN KEY(habit_id) REFERENCES habits(id)
            )
        """

    insert_statement = """
        INSERT INTO habit_completions (habit_id, completion_date, period_number) VALUES (?, ?, ?)
    """

    select_statement = """
        SELECT * FROM habit_completions WHERE habit_id = ?
    """

    def __init__(self, habit :Habit = None, completion_date: datetime=None, period_number: int = None, id: int = None):
        self.id = id
        if habit is None:
            return

        self.habit_id = habit.id
        self.completion_date = datetime.now()

        self.period_number= self.calc_period_number(habit, self.completion_date)

    @staticmethod
    def calc_period_number(habit: Habit,completion_date :datetime = datetime.now()):
        #start date is yy mm dd
        start_date=habit.get_start_date()

        if habit.period == Period.DAILY:
            return (completion_date - start_date).days
        elif habit.period == Period.WEEKLY:
            return (completion_date - start_date).days // 7

    def save(self):
        cursor = self.db.connect().cursor()
        cursor.execute(self.insert_statement, (
            self.habit_id,
            self.completion_date.isoformat(),
            self.period_number
        ))
        self.db.connect().commit()
        #get id
        self.id = cursor.lastrowid
        return True;


    @staticmethod
    def get(habit_id: int):
        cursor = HabitCompletion.db.connect().cursor()
        cursor.execute(HabitCompletion.select_statement, (habit_id,))
        results = cursor.fetchall()
        if results:
            completions = []
            for row in results:
                habit_completion = HabitCompletion(
                    Habit.get(row[1]),  # Retrieve the Habit instance
                    completion_date=datetime.fromisoformat(row[2]),
                    period_number=row[3],
                    id=row[0]
                )
                completions.append(habit_completion)

            return completions
        else:
            return None


    def __repr__(self):
        return f"HabitCompletion( id={self.id}, habit_id={self.habit_id}, completion_date='{self.completion_date}', period_number={self.period_number} )"
