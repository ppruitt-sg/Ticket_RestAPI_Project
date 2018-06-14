import sqlite3
from flask import jsonify


class AccountModel():
    filename = 'data.db'

    def __init__(self, username, password, id=0):
        self.username = username
        self.password = password
        self.id = id

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def add_to_db(self):
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()

        query = "INSERT INTO auth (username, password) VALUES (?, ?)"
        cursor.execute(query, (self.username, self.password))
        self.id = cursor.lastrowid

        conn.commit()
        conn.close()

    def delete_from_db(self):

        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()

        query = "DELETE FROM auth WHERE id=?"
        cursor.execute(query, (self.id,))

        conn.commit()
        conn.close()

    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect(cls.filename)
        cursor = conn.cursor()

        query = "SELECT username, password, id FROM auth WHERE username=?"
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(row[0], row[1], row[2])

    @classmethod
    def find_by_id(cls, id):
        conn = sqlite3.connect(cls.filename)
        cursor = conn.cursor()

        query = "SELECT username, password, id FROM auth WHERE id=?"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(row[0], row[1], row[2])
