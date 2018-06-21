import os

from flask import Flask
from flask_restful import Api, reqparse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_jwt_extended import JWTManager

from resources.random_json import RandomJSON
from resources.random_csv import RandomCSV

from resources.employee import (Employee,
                                EmployeeTickets,
                                EmployeeEmail,
                                EmployeeCreator)
from resources.customer import (Customer,
                                CustomerTickets,
                                CustomerEmail,
                                CustomerCreator)
from resources.ticket import Ticket, TicketCreator, TicketAssigner
from resources.comment import Comment, CommentAdder
from resources.account import AccountRegister, Account, AccountLogin


app = Flask(__name__)
app.config['PROPOGATE_EXCEPTIONS'] = True
limiter = Limiter(default_limits=["1000/hour"],
                  key_func=get_remote_address, headers_enabled=True)
limiter.init_app(app)
app.secret_key = 'poul'
api = Api(app)

jwt = JWTManager(app)


@api.representation('text/csv')
def output_csv(data, code, headers=None):
    pass


# Random sink addresses
api.add_resource(RandomJSON, '/random/json/<int:amount>')
api.add_resource(RandomCSV, '/random/csv/<int:amount>')

# Ticket API
api.add_resource(Customer, '/customer/<int:id>')
api.add_resource(CustomerTickets, '/customer/<int:id>/tickets')
api.add_resource(CustomerEmail, '/customer/email/<string:email>')
api.add_resource(CustomerCreator, '/customer')

api.add_resource(Employee, '/employee/<int:id>')
api.add_resource(EmployeeTickets, '/employee/<int:id>/tickets')
api.add_resource(EmployeeEmail, '/employee/email/<string:email>')
api.add_resource(EmployeeCreator, '/employee')

api.add_resource(Ticket, '/tickets/<int:number>')
api.add_resource(TicketCreator, '/tickets/new')
api.add_resource(TicketAssigner, '/tickets/<int:number>/assign')

api.add_resource(CommentAdder, '/tickets/<int:number>/comment')
api.add_resource(Comment, '/tickets/<int:number>/comments')

api.add_resource(AccountRegister, '/register')
api.add_resource(Account, '/account/<int:user_id>')
api.add_resource(AccountLogin, '/login')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
