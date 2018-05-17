import sqlite3
from flask import jsonify

class UserModel():
	filename = 'data.db'

	def __init__(self, email, name, is_customer, id=0):
		self.email = email
		self.name = name
		self.id=id

		if is_customer == True:
			self.table_name = "customers"
		elif is_customer == False:
			self.table_name = "employees"

	def json(self):
		return {'id': self.id, 'email': self.email, 'name': self.name}

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
			return cls(row[0], row[1], is_customer, row[2]) # row[0], row[1], row[2] are email, name, id

	@classmethod
	def find_by_id(cls, id, is_customer):
		if is_customer:
			table_name = "customers"
		else:
			table_name = "employees"

		conn = sqlite3.connect(cls.filename)
		cursor = conn.cursor()

		query = "SELECT email, name, id FROM {} WHERE id=?".format(table_name)
		cursor.execute(query, (id,))
		row = cursor.fetchone()
		conn.close()

		if row:
			return cls(row[0], row[1], is_customer, row[2]) # row[0], row[1], row[2] are email, name, id

	def add_to_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "INSERT INTO {} (email, name) VALUES (?, ?)".format(self.table_name)
		cursor.execute(query, (self.email, self.name))
		self.id = cursor.lastrowid

		conn.commit()
		conn.close()

	def update_to_db(self):

		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "UPDATE {} SET name=? WHERE email=?".format(self.table_name)
		cursor.execute(query, (self.name, self.email))

		conn.commit()
		conn.close()

	def delete_from_db(self):

		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "DELETE FROM {} WHERE email=?".format(self.table_name)
		cursor.execute(query, (self.email,))

		conn.commit()
		conn.close()