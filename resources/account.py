from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity
)

from models.account import AccountModel

_account_parser = reqparse.RequestParser()
_account_parser.add_argument('username',
                             type=str,
                             required=True,
                             help="This field cannot be blank!"
                             )
_account_parser.add_argument('password',
                             type=str,
                             required=True,
                             help="This field cannot be blank!"
                             )


class AccountRegister(Resource):

    def post(self):
        data = _account_parser.parse_args()

        if AccountModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        account = AccountModel(**data)
        account.add_to_db()

        return {"message": "Account created successfully."}, 201


class Account(Resource):

    @classmethod
    def get(cls, user_id):
        account = AccountModel.find_by_id(user_id)
        if not account:
            return {'message': 'Account not found'}, 404
        return account.json()

    @classmethod
    def delete(cls, user_id):
        account = AccountModel.find_by_id(user_id)
        if not account:
            return {'message': 'Account not found'}, 404
        account.delete_from_db()
        return {'message': 'Account deleted'}, 200


class AccountLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        data = _account_parser.parse_args()
        # find user in database
        account = AccountModel.find_by_username(data['username'])
        # check password
        if account and safe_str_cmp(account.password, data['password']):
            access_token = create_access_token(identity=account.id, fresh=True)
            return {
                'access_token': access_token
            }, 200

            return {'message': 'Invalid credentials'}, 401
