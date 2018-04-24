import sqlite3
from flask import jsonify

class CustomerModel():
	filename = 'data.db'

	def __init__(self, email, name, id=0):
		self.email = email
		self.name = name
		self.id=id

	def json(self):
		return {'email': self.email, 'name': self.name}

	@classmethod
	def find_by_email(cls, email):
		conn = sqlite3.connect(cls.filename)
		cursor = conn.cursor()

		query = "SELECT email, name, id FROM customers WHERE email=?"
		cursor.execute(query, (email,))
		row = cursor.fetchone()
		conn.close()

		if row:
			return cls(*row) # row[0], Row[1] are email, name

	def find_tickets(self):
		pass

	def add_to_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "INSERT INTO customers (email, name) VALUES (?, ?)"
		cursor.execute(query, (self.email, self.name))

		conn.commit()
		conn.close()

	def update_to_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "UPDATE customers SET name=? WHERE email=?"
		cursor.execute(query, (self.name, self.email))

		conn.commit()
		conn.close()

	def delete_from_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "DELETE FROM customers WHERE email=?"
		cursor.execute(query, (self.email,))

		conn.commit()
		conn.close()