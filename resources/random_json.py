from flask_restful import Resource, reqparse
from flask.json import jsonify

from models.random_sink import RandomSink


class RandomJSON(Resource):

    def get(self, amount):
        if amount > 0 and amount <= 100000:
            emails = RandomSink.get_emails(amount)
            return jsonify({"emails": emails})
        return {"message": "Must be between 1 and 100,000"}, 404
