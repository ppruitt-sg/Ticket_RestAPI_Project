from resources.user import User, UserTickets, UserEmail, UserCreator
from flask_jwt_extended import jwt_required


class Customer(User):

    def get(self, id):
        return super().get(id, is_customer=True)

    def patch(self, id):
        return super().patch(id, is_customer=True)

    @jwt_required
    def delete(self, id):
        return super().delete(id, is_customer=True)


class CustomerTickets(UserTickets):

    def get(self, id):
        return super().get(id, is_customer=True)


class CustomerEmail(UserEmail):

    def get(self, email):
        return super().get(email, is_customer=True)


class CustomerCreator(UserCreator):

    def post(self):
        return super().post(is_customer=True)
