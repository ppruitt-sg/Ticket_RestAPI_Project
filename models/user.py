import sqlite3
from flask import jsonify

class UserModel():
	filename = 'data.db'

	def __init__(self, email, name, id=0, user_type=None):
		self.email = email
		self.name = name
		self.id=id
		self.user_type = user_type

	def json(self):
		return {'email': self.email, 'name': self.name}

	@classmethod
	def find_by_email(cls, user_type, email):
		if user_type == "customer":
			table_name = "customers"
		elif user_type == "employee":
			table_name = "employees"
		else:
			raise ValueError("Invalid user_type")

		conn = sqlite3.connect(cls.filename)
		cursor = conn.cursor()

		query = "SELECT email, name, id FROM {} WHERE email=?".format(table_name)
		cursor.execute(query, (email,))
		row = cursor.fetchone()
		conn.close()

		if row:
			return cls(*row, user_type) # row[0], Row[1] are email, name

	def find_tickets(self):
		pass

	def add_to_db(self):
		if self.user_type == "customer":
			table_name = "customers"
		elif self.user_type == "employee":
			table_name = "employees"
		else:
			raise ValueError("Invalid user_type")

		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "INSERT INTO {} (email, name) VALUES (?, ?)".format(table_name)
		cursor.execute(query, (self.email, self.name))

		conn.commit()
		conn.close()

	def update_to_db(self):
		if self.user_type == "customer":
			table_name = "customers"
		elif self.user_type == "employee":
			table_name = "employees"
		else:
			raise ValueError("Invalid user_type")

		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "UPDATE {} SET name=? WHERE email=?".format(table_name)

		cursor.execute(query, (self.name, self.email))

		conn.commit()
		conn.close()

	def delete_from_db(self):
		if self.user_type == "customer":
			table_name = "customers"
		elif self.user_type == "employee":
			table_name = "employees"
		else:
			raise ValueError("Invalid user_type")

		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "DELETE FROM {} WHERE email=?".format(table_name)
		cursor.execute(query, (self.email,))

		conn.commit()
		conn.close()