import os

from flask import Flask
from flask_restful import Api, reqparse

from resources.random_json import RandomJSON
from resources.random_csv import RandomCSV

from resources.user import User, UserTickets, UserCreator, UserEmail
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
api.add_resource(User, '/<string:user_type>/<int:id>')
api.add_resource(UserTickets, '/<string:user_type>/<string:email>/tickets')
api.add_resource(UserCreator, '/<string:user_type>')
api.add_resource(UserEmail, '/<string:user_type>/email/<string:email>')

api.add_resource(Ticket, '/tickets/<int:number>')
api.add_resource(TicketCreator, '/tickets/new')
api.add_resource(TicketAssigner, '/tickets/<int:number>/assign')

api.add_resource(Comment, '/tickets/<int:number>/comment')



if __name__ == '__main__':
	app.run(port=5000, debug=True)
