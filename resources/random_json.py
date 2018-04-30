from flask_restful import Resource, reqparse
from flask.json import jsonify

from  models.random_sink import RandomSink

class RandomJSON(Resource):
	def get(self, amount):
		if amount > 0 and amount <= 1000000:
			emails = RandomSink.get_emails(amount)
			return jsonify({"email": emails})
		return {"message": "Must be between 1 and 1,000,000"}, 404