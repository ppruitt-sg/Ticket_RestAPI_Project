from flask_restful import Resource, reqparse

from models.customer import CustomerModel
from models.ticket import TicketModel

class Customer(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('name',
		type=str,
		required=False,
		help="This field cannot be blank!"
	)

	def get(self, email):
		customer = CustomerModel.find_by_email(email)
		if customer:
			return customer.json()
		return {'message': 'Email not found'}, 404

	def post(self, email):
		if CustomerModel.find_by_email(email):
			return {'message': "Email '{}' already exists.".format(email)}, 400

		data = Customer.parser.parse_args()

		customer = CustomerModel(email, data['name'])
		
		try:
			customer.add_to_db()
		except:
			return {"message": "An error occurred inserting the item."}, 500

		return customer.json(), 201


	def patch(self, email):
		customer = CustomerModel.find_by_email(email)
		if customer:
			data = Customer.parser.parse_args()
			customer.name = data['name']

			try:
				customer.update_to_db()
			except:
				return {"message": "An error occurred inserting the item."}, 500

			return customer.json(), 201

		return {'message': 'Email not found'}, 404



	def delete(self, email):
		customer = CustomerModel.find_by_email(email)
		if customer:
			customer.delete_from_db()

		return {"message": "Email deleted"}

class CustomerTickets(Resource):
	def get(self, email):
		customer = CustomerModel.find_by_email(email)
		if customer:
			return { "tickets": [ticket.json() for ticket in TicketModel.find_by_email(email, customer=True)]}
		return { "tickets": []}
