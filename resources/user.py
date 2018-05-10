from flask_restful import Resource, reqparse

from models.user import UserModel
from models.ticket import TicketModel

class User(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('name',
		type=str,
		required=False,
		help="This field cannot be blank!"
	)

	def get(self, user_type, email):
		try:
			user = UserModel.find_by_email(user_type, email)
		except:
			return {}, 404

		if user:
			return user.json()
		return {'message': 'Email not found'}, 404

	def post(self, user_type, email):
		try:
			if UserModel.find_by_email(user_type, email):
				return {'message': "Email '{}' already exists.".format(email)}, 400
		except:
			return {}, 404

		data = User.parser.parse_args()

		user = UserModel(email, data['name'], user_type=user_type)
		
		try:
			user.add_to_db()
		except:
			return {"message": "An error occurred inserting the item."}, 500

		return user.json(), 201


	def patch(self, user_type, email):
		try:
			user = UserModel.find_by_email(user_type, email)
		except:
			return {}, 404

		if user:
			data = User.parser.parse_args()
			user.name = data['name']

			try:
				user.update_to_db()
			except:
				return {"message": "An error occurred inserting the item."}, 500

			return user.json(), 201

		return {'message': 'Email not found'}, 404



	def delete(self, user_type, email):
		try:
			user = UserModel.find_by_email(user_type, email)
		except:
			return {}, 404

		if user:
			user.delete_from_db()

		return {"message": "Email deleted"}

class UserTickets(Resource):
	def get(self, user_type, email):
		try:
			user = UserModel.find_by_email(user_type, email)
		except:
			return {}, 404

		if user_type == "customer":
			is_customer = True
		else:
			is_customer = False
		
		if user:
			return { "tickets": [ticket.json() for ticket in TicketModel.find_by_email(email, is_customer)]}
		return { "tickets": []}
