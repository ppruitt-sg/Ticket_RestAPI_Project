import sqlite3
from flask import jsonify

class EmployeeModel():
	filename = 'data.db'

	def __init__(self, email, name, id=0):
		self.email = email
		self.name = name
		self.id = id

	def json(self):
		return {'email': self.email, 'name': self.name}

	@classmethod
	def find_by_email(cls, email):
		conn = sqlite3.connect(cls.filename)
		cursor = conn.cursor()

		query = "SELECT email, name, id FROM employees WHERE email=?"
		cursor.execute(query, (email,))
		row = cursor.fetchone()
		conn.close()

		if row:
			return cls(*row)

	def add_to_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "INSERT INTO employees (email, name) VALUES (?, ?)"
		cursor.execute(query, (self.email, self.name))

		conn.commit()
		conn.close()

	def update_to_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "UPDATE employees SET name=? WHERE email=?"
		cursor.execute(query, (self.name, self.email))

		conn.commit()
		conn.close()

	def delete_from_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "DELETE FROM employees WHERE email=?"
		cursor.execute(query, (self.email,))

		conn.commit()
		conn.close()
