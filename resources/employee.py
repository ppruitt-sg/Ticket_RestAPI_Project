from resources.user import User, UserTickets, UserEmail, UserCreator

from flask_jwt_extended import jwt_required


class Employee(User):

    def get(self, id):
        return super().get(id, is_customer=False)

    def patch(self, id):
        return super().patch(id, is_customer=False)

    @jwt_required
    def delete(self, id):
        return super().delete(id, is_customer=False)


class EmployeeTickets(UserTickets):

    def get(self, id):
        return super().get(id, is_customer=False)


class EmployeeEmail(UserEmail):

    def get(self, email):
        return super().get(email, is_customer=False)


class EmployeeCreator(UserCreator):

    @jwt_required
    def post(self):
        return super().post(is_customer=False)
