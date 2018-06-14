from flask_restful import Resource, reqparse
from flask.json import jsonify
from flask import Response

from models.random_sink import RandomSink


class RandomCSV(Resource):

    def get(self, amount):
        if amount > 0 and amount <= 100000:
            emails = RandomSink.get_emails(amount)
            return Response("email\n" + "\n".join(emails), mimetype='text/csv')
        return {"message": "Must be between 1 and 100,000"}, 404
