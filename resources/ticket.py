import time
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.user import UserModel
from models.ticket import TicketModel
from models.comment import CommentModel

from resources.comment import Comment


class Ticket(Resource):

    def get(self, number):
        # Returns ticket with that specific number
        ticket = TicketModel.find_by_number(number)
        if ticket:
            return ticket.json()
        return {'message': 'Ticket not found'}, 404

    @jwt_required
    def delete(self, number):
        # Deletes ticket if it exists
        ticket = TicketModel.find_by_number(number)
        if ticket:
            ticket.delete_from_db()
        return {'message': 'Ticket deleted'}


class TicketCreator(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('subject',
                        type=str,
                        required=True,
                        help="Subject is required.")
    parser.add_argument('content',
                        type=str,
                        required=True,
                        help="Content is required.")
    parser.add_argument('customer',
                        type=str,
                        required=True,
                        help="Customer email is required.")

    def post(self):
        # Creates new tickets
        data = TicketCreator.parser.parse_args()
        customer = UserModel.find_by_email(data['customer'], is_customer=True)

        # Check if username exists
        if customer:
            # Create ticket
            ticket = TicketModel(customer.id, data['subject'])

            try:
                ticket.add_to_db()
            except IntegrityError:
                return {"message":
                        "An error occurred inserting the item."}, 500

            # Add comment
            timestamp = int(time.time())
            comment = CommentModel(
                ticket.number, timestamp, customer.email, data['content'])

            try:
                comment.add_to_db()
            except IntegrityError:
                return {"message":
                        "An error occurred inserting the item."}, 500

            return ticket.json(), 201

        return {"message": "Customer not found"}, 400


class TicketAssigner(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('employee',
                        type=str,
                        required=True,
                        help="Email is required")

    def patch(self, number):
        # Assigns employee to specific ticket, if it exists
        ticket = TicketModel.find_by_number(number)
        if ticket:
        # Checks if ticket exists
            data = TicketAssigner.parser.parse_args()
            employee = UserModel.find_by_email(
                data['employee'], is_customer=False)
            if employee:
            # Checks if employee exists
                ticket.employee_id = employee.id
                try:
                    ticket.update_to_db()
                except IntegrityError:
                    return {"message":
                        "An error occurred inserting the item."}, 500

                return ticket.json()

            return {"message": "Employee not found"}, 400
        return {"message": "Ticket not found"}, 404
