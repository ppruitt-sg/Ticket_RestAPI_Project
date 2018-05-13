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

	def get(self, id, is_customer):
		user = UserModel.find_by_id(id, is_customer)

		if user:
			return user.json(), 200
		return {'message': 'ID not found'}, 404


	def patch(self, id, is_customer):
		user = UserModel.find_by_id(id, is_customer)

		if user:
			data = User.parser.parse_args()
			user.name = data['name']

			try:
				user.update_to_db()
			except:
				return {"message": "An error occurred inserting the item."}, 500

			return user.json(), 201

		return {'message': 'Email not found'}, 404

	def delete(self, id, is_customer):
		user = UserModel.find_by_id(id, is_customer)

		if user:
			user.delete_from_db()

		return {"message": "Email deleted"}


class UserTickets(Resource):
	def get(self, email, is_customer):
		user = UserModel.find_by_email(email, is_customer)
		
		if user:
			return { "tickets": [ticket.json() for ticket in TicketModel.find_by_email(email, is_customer)]}
		return { "tickets": []}


class UserEmail(Resource):
	def get(self, email, is_customer):
		user = UserModel.find_by_email(email, is_customer)

		if user:
			return user.json(), 200
		return {'message': 'email not found'}, 404


class UserCreator(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('email',
		type=str,
		required=False,
		help="This field cannot be blank!"
	)
	parser.add_argument('name',
		type=str,
		required=False,
		help="This field cannot be blank!"
	)

	def post(self, is_customer):
		data = UserCreator.parser.parse_args()

		user = UserModel.find_by_email(data['email'], is_customer)

		if user:
			return {"message": "User already exists"}, 404
		user = UserModel(data['email'], data['name'], is_customer=is_customer)
		
		try:
			user.add_to_db()
		except:
			return {"message": "An error occurred inserting the item."}, 500

		return user.json(), 201

