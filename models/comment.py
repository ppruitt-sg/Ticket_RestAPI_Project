import sqlite3

class CommentModel():
	filename = 'data.db'

	def __init__(self, number, timestamp, from_email, content):
		self.number = number
		self.timestamp = timestamp
		self.from_email = from_email
		self.content = content

	@classmethod
	def find_by_number(cls, number):
		conn = sqlite3.connect(cls.filename)
		cursor = conn.cursor()

		query = "SELECT number, timestamp, from_email, content FROM comments WHERE number=?"
		cursor.execute(query, (number,))
		rows = cursor.fetchall()
		conn.close()

		if rows:
			return [CommentModel(*row).json() for row in rows]

	def json(self):
		return {'timestamp': self.timestamp, 'from_email': self.from_email, 'content': self.content}

	def add_to_db(self):
		conn = sqlite3.connect(self.filename)
		cursor = conn.cursor()

		query = "INSERT INTO comments (number, timestamp, from_email, content) VALUES (?, ?, ?, ?)"
		cursor.execute(query, (self.number, self.timestamp, self.from_email, self.content))

		conn.commit()
		conn.close()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()