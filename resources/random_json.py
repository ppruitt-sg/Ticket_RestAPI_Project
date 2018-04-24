from flask_restful import Resource, reqparse
from flask.json import jsonify

from  models.random_sink import RandomSink

class RandomJSON(Resource):
	def get(self, amount):
		emails = RandomSink.get_emails(amount)
		return jsonify({"email": emails})