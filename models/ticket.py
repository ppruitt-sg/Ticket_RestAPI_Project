import sqlite3

from models.comment import CommentModel

class TicketModel():
	filename='data.db'

	def __init__(self, customer_id, subject, number=None, employee_id=None):
		self.customer_id = customer_id
		self.subject = subject
		self.number = number
		self.employee_id = employee_id


	def json(self):
		return {"number": self.number,\
				"customer_id": self.customer_id,\
				"subject": self.subject,
				"employee_id": self.employee_id}

	@classmethod
	def find_by_number(cls, number):
		conn = sqlite3.connect(cls.filename)
		cursor = conn.cursor()

		query = "SELECT customer_id, subject, number, employee_id FROM tickets WHERE number=?"
		cursor.execute(query, (number,))
		row = cursor.fetchone()
		
		conn.close()

		if row:
			return cls(*row)


	def add_to_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "INSERT INTO tickets (customer_id, subject) VALUES (?, ?)"
		cursor.execute(query, (self.customer_id, self.subject))
		self.number = cursor.lastrowid # Ticket number corresponds with row ID

		conn.commit()
		conn.close()

	def update_to_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "UPDATE tickets SET customer_id=?, subject=?, employee_id=? WHERE number=?"
		cursor.execute(query, (self.customer_id, self.subject, self.employee_id, self.number))
		
		conn.commit()
		conn.close()

	def delete_from_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "PRAGMA foreign_keys = ON"
		cursor.execute(query)

		query = "DELETE FROM tickets WHERE number=?"
		cursor.execute(query, (self.number,))

		conn.commit()
		conn.close()
