import sqlite3
class DATABASE:
    connection= None
    def __init__(self):
        if DATABASE.connection is None:
            DATABASE.connection=sqlite3.connect("habit_tracing_app.db")

    def connect(self):
        return DATABASE.connection

    def create_tables(self,classes):
        with DATABASE.connection:
            for cls in classes:
                DATABASE.connection.execute(cls.table(cls))
