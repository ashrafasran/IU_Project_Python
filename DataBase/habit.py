from datetime import datetime
from enum import Enum
from DataBase.database import DATABASE

class Period(Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'

class Habit:
    db = DATABASE()

    def table(self):
        return """
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                period TEXT NOT NULL,
                created_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """

    insert_statement = "INSERT INTO habits (user_id, title, description, period) VALUES (?, ?, ?, ?)"
    update_statement = "UPDATE habits SET title = ?, description = ?, period = ? WHERE id = ?"
    delete_statement = "DELETE FROM habits WHERE id = ?"

    select_statement = "SELECT * FROM habits WHERE user_id = ?"

    def __init__(self, user_id: int, title: str, description: str = None,
                 period: Period = Period.DAILY, id: int = None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.period = period

    def save(self):
        cursor = self.db.connect().cursor()
        cursor.execute(self.insert_statement, (self.user_id, self.title,
                                               self.description, self.period.value))
        self.db.connect().commit()
        self.id = cursor.lastrowid
        return  True

    def update(self, title: str = None, description: str = None, period: Period = None):
        if title:
            self.title = title
        if description:
            self.description = description
        if period:
            self.period = period
        cursor = self.db.connect().cursor()
        cursor.execute(self.update_statement, (self.title, self.description,
                                               self.period.value, self.id))
        self.db.connect().commit()
        return True

    @staticmethod
    # delete by habit_id
    def delete(habit_id: str):
        cursor = Habit.db.connect().cursor()
        cursor.execute(Habit.delete_statement, (habit_id,))
        Habit.db.connect().commit()
        return True

    @staticmethod
    def get_all_habits(user_id: int):
        cursor = Habit.db.connect().cursor()
        cursor.execute(Habit.select_statement, (user_id,))
        results = cursor.fetchall()
        if results:
            habits = []
            for row in results:
                habit = Habit(
                    user_id=row[1],
                    title=row[2],
                    description=row[3],
                    period=Period(row[4]),
                    id=row[0]
                )
                habits.append(habit)
            return habits
        else:
            print(f"Habits for user id ({user_id}) not found.")
            return None

    @staticmethod
    def get(habit_id:int):
        cursor = Habit.db.connect().cursor()
        cursor.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
        results = cursor.fetchone()
        if results:
            return Habit(user_id=results[1], title=results[2], description=results[3],
                          period=Period(results[4]), id=results[0])
        else:
            print(f"Habit with id ({habit_id}) not found.")
            return None


    def get_start_date(self):
        cursor = self.db.connect().cursor()
        cursor.execute("SELECT created_datetime FROM habits WHERE id = ?", (self.id,))
        result = cursor.fetchone()
        if result:
            return datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        else:
            print(f"Habit with id ({self.id}) not found.")
            return None


    def __repr__(self):
        return f"Habit(id={self.id}, title='{self.title}', description='{self.description}', period='{self.period.value}')"
