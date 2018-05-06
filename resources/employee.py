from flask_restful import Resource, reqparse

from models.employee import EmployeeModel
from models.ticket import TicketModel

class Employee(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('name',
		type=str,
		required=False,
		help="This field cannot be blank!"
	)

	def get(self, email):
		employee = EmployeeModel.find_by_email(email)
		if employee:
			return employee.json()
		return {'message': 'Email not found'}, 404

	def post(self, email):
		if EmployeeModel.find_by_email(email):
			return {'message': "Email '{}' already exists.".format(email)}, 400

		data = Employee.parser.parse_args()

		employee = EmployeeModel(email, data['name'])
		
		try:
			employee.add_to_db()
		except:
			return {"message": "An error occurred inserting the item."}, 500

		return employee.json(), 201


	def patch(self, email):
		employee = EmployeeModel.find_by_email(email)
		if employee:
			data = Employee.parser.parse_args()
			employee.name = data['name']

			try:
				employee.update_to_db()
			except:
				return {"message": "An error occurred inserting the item."}, 500

			return employee.json(), 201

		return {'message': 'Email not found'}, 404



	def delete(self, email):
		employee = EmployeeModel.find_by_email(email)
		if employee:
			employee.delete_from_db()

		return {"message": "Email deleted"}

class EmployeeTickets(Resource):
	def get(self, email):
		employee = EmployeeModel.find_by_email(email)
		if employee:
			return { "tickets": [ticket.json() for ticket in TicketModel.find_by_email(email, customer=False)]}
		return { "tickets": []}
