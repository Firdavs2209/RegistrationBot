import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def __add_new_user(self, tg_id, email, birth_year):
        self.cursor.execute(f"INSERT INTO users(tg_id, email, birth_year) "
                            f"VALUES (?, ?, ?)", (tg_id, email, birth_year))
        self.connection.commit()

    def update_user(self, tg_id, full_name, phone):
        self.cursor.execute(f"UPDATE users SET tg_full_name=?, tg_phone=? "
                            f"WHERE tg_id=?", (full_name, phone, tg_id))
        self.connection.commit()

    def get_user(self, tg_id):
        users = self.cursor.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
        return users.fetchone()

    def get_user_by_email(self, email):
        users = self.cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        return users.fetchone()

    def add_new_user(self, tg_id, email, birth_year):

        self.__add_new_user(tg_id, email, birth_year)

    def __del__(self):
        self.cursor.close()
        self.connection.close()


