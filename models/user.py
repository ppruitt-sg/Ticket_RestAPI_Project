import sqlite3
from flask import jsonify

class UserModel():
	filename = 'data.db'

	def __init__(self, email, name, id=0, is_customer=None):
		self.email = email
		self.name = name
		self.id=id
		self.is_customer=is_customer

	def json(self):
		return {'email': self.email, 'name': self.name}

	@classmethod
	def find_by_email(cls, email, is_customer):
		if is_customer:
			table_name = "customers"
		else:
			table_name = "employees"

		conn = sqlite3.connect(cls.filename)
		cursor = conn.cursor()

		query = "SELECT email, name, id FROM {} WHERE email=?".format(table_name)
		cursor.execute(query, (email,))
		row = cursor.fetchone()
		conn.close()

		if row:
			return cls(*row, is_customer) # row[0], row[1], row[2] are email, name, id

	def find_tickets(self):
		pass

	def add_to_db(self):
		if self.is_customer:
			table_name = "customers"
		else:
			table_name = "employees"

		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "INSERT INTO {} (email, name) VALUES (?, ?)".format(table_name)
		cursor.execute(query, (self.email, self.name))

		conn.commit()
		conn.close()

	def update_to_db(self):
		if self.is_customer:
			table_name = "customers"
		else:
			table_name = "employees"

		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "UPDATE {} SET name=? WHERE email=?".format(table_name)

		cursor.execute(query, (self.name, self.email))

		conn.commit()
		conn.close()

	def delete_from_db(self):
		if self.is_customer:
			table_name = "customers"
		else:
			table_name = "employees"

		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "DELETE FROM {} WHERE email=?".format(table_name)
		cursor.execute(query, (self.email,))

		conn.commit()
		conn.close()