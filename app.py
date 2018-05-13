import os

from flask import Flask
from flask_restful import Api, reqparse

from resources.random_json import RandomJSON
from resources.random_csv import RandomCSV

from resources.employee import Employee, EmployeeTickets, EmployeeEmail, EmployeeCreator
from resources.customer import Customer, CustomerTickets, CustomerEmail, CustomerCreator
from resources.ticket import Ticket, TicketCreator, TicketAssigner
from resources.comment import Comment


app = Flask(__name__)
app.secret_key = 'poul'
api = Api(app)

@api.representation('text/csv')
def output_csv(data, code, headers=None):
	pass

# Random sink addresses
api.add_resource(RandomJSON, '/random/json/<int:amount>')
api.add_resource(RandomCSV, '/random/csv/<int:amount>')

# Ticket API
api.add_resource(Customer, '/customer/<int:id>')
api.add_resource(CustomerTickets, '/customer/<string:email>/tickets')
api.add_resource(CustomerEmail, '/customer/email/<string:email>')
api.add_resource(CustomerCreator, '/customer')

api.add_resource(Employee, '/employee/<int:id>')
api.add_resource(EmployeeTickets, '/employee/<string:email>/tickets')
api.add_resource(EmployeeEmail, '/employee/email/<string:email>')
api.add_resource(EmployeeCreator, '/employee')

api.add_resource(Ticket, '/tickets/<int:number>')
api.add_resource(TicketCreator, '/tickets/new')
api.add_resource(TicketAssigner, '/tickets/<int:number>/assign')

api.add_resource(Comment, '/tickets/<int:number>/comment')


if __name__ == '__main__':
	app.run(port=5000, debug=True)
