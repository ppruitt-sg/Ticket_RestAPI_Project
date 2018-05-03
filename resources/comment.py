from flask_restful import Resource, reqparse
import time

from models.ticket import TicketModel
from models.comment import CommentModel

class Comment(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('from_email',
		type=str,
		required=True,
		help="From email must be included.")
	parser.add_argument('content',
		type=str,
		required=True,
		help="Comment content must be included.")

	def patch(self, number):
		data = Comment.parser.parse_args()
		ticket = TicketModel.find_by_number(number)
		if ticket:
			timestamp = int(time.time())
			comment = CommentModel(number, timestamp, **data)

			try:
				comment.add_to_db()
			except:
				return {"message": "An error occurred inserting the item."}, 500

			return comment.json(), 202

		return {"message": "Ticket not found"}, 400

	def get(self, number):
		comments = CommentModel.find_by_number(number)

		if comments:
			return {"comments": comments}

		return {"message": "Ticket not found."}
