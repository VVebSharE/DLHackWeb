# images of a user
# imageurl, username, time, imageinferedurl

# auth
# username, password


import sqlite3
import os
import datetime

class Database:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect("database.db", check_same_thread=False)
            cls._instance.cursor = cls._instance.conn.cursor()
            cls._instance.create_table()
        return cls._instance

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_url TEXT NOT NULL,
                imageinferedurl TEXT NOT NULL,
                username TEXT NOT NULL,
                time TEXT NOT NULL
            )
        """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """
        )

        self.conn.commit()

    def add_image(
        self, image_url, imageinferedurl, username
    ):  # Fixed parameter order
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            """
            INSERT INTO images (image_url, imageinferedurl, username, time) VALUES (?, ?, ?, ?)
        """,
            (image_url, imageinferedurl, username, time),
        )  # Added imageinferedurl

        self.conn.commit()

    def get_images(self, username):
        self.cursor.execute(
            """
            SELECT * FROM images WHERE username = ?
        """,
            (username,),
        )

        return self.cursor.fetchall()

    def add_user(self, username, password):
        self.cursor.execute(
            """
            INSERT INTO users (username, password) VALUES (?, ?)
        """,
            (username, password),
        )

        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute(
            """
            SELECT * FROM users WHERE username = ?
        """,
            (username,),
        )

        # return as {'username': 'user10', 'password': 'password'}
        user_data = self.cursor.fetchone()
        if not user_data:
            return None

        return {"username": user_data[1], "password": user_data[2]}

db = Database()
db.create_table()

if __name__ == '__main__':
   print(db.get_user('user1'))
