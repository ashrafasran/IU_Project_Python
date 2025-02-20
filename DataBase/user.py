from DataBase.database import DATABASE

class USER:
    db = DATABASE()

    def table(self):
        return """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """

    insert_statement = "INSERT INTO users (name, email, password) VALUES (?, ?, ?)"
    update_statement = "UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?"
    delete_statement = "DELETE FROM users WHERE id = ?"
    select_statement = "SELECT * FROM users where email = ? "

    def __init__(self, name: str = None, email: str = None, password: str = None, id: int = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def save(self):
        cursor = self.db.connect().cursor()
        cursor.execute(self.table())
        if USER.email_exist(self.email):
            print(f"Email {self.email} already exists.")
            return False
        else:
            cursor.execute(self.insert_statement, (self.name, self.email, self.password))
            self.db.connect().commit()
            self.id = cursor.lastrowid
            print(f"User {self.email} saved successfully with ID {self.id}.")
            return True

    def update(self, name:str =None, password:str =None):
        if name:
            self.name = name
        if password:
            self.password = password
        cursor = self.db.connect().cursor()
        cursor.execute(self.update_statement, (self.name, self.email, self.password, self.id))
        self.db.connect().commit()
        return True

    @staticmethod
    def email_exist(email: str):
        cursor = USER.db.connect().cursor()
        cursor.execute(USER.select_statement, (email,))
        result = cursor.fetchone()
        if result:
            print(f"this email ({email}) is occupied, try another one.")
            return True
        else:
            return False

    @staticmethod
    def delete(email: str):
        current_user = USER.get(email)
        if current_user is None:
            return False
        else:
            cursor = USER.db.connect().cursor()
            cursor.execute(USER.delete_statement, (current_user.id,))
            USER.db.connect().commit()
            return True

    @staticmethod
    def get(email: str):
        cursor = USER.db.connect().cursor()
        cursor.execute(USER.select_statement, (email,))
        result = cursor.fetchone()
        if result:
            return USER(id=result[0], name=result[1], email=result[2], password=result[3])
        else:
            print(f"User with email ({email}) not found.")
            return None

    def __repr__(self):
        return f"User(id = {self.id}, name = {self.name}, email = {self.email})"