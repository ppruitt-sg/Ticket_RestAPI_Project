import sqlite3

from models.comment import CommentModel

class TicketModel():
	filename='data.db'

	# number = db.Column(db.Integer, primary_key=True)
	# customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
	# employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
	# subject = db.Column(db.String(100))

	# #responses = db.relationship('ResponseModel', lazy='dynamic')
	# customer = db.relationship('CustomerModel', lazy=True)
	# employee = db.relationship('EmployeeModel', lazy=True)

	def __init__(self, customer_id, subject, number=None):
		self.customer_id = customer_id
		self.subject = subject
		self.number = number
		self.employee_id = None


	def json(self):
		return {"number": self.number,\
				"customer_id": self.customer_id,\
				"subject": self.subject,\
				"responses": CommentModel.find_by_number(self.number)}

	@classmethod
	def find_by_number(cls, number):
		conn = sqlite3.connect(cls.filename)
		cursor = conn.cursor()

		query = "SELECT customer_id, subject, number FROM tickets WHERE number=?"
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

	def delete_from_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "PRAGMA foreign_keys = ON"
		cursor.execute(query)

		query = "DELETE FROM tickets WHERE number=?"
		cursor.execute(query, (self.number,))

		conn.commit()
		conn.close()
