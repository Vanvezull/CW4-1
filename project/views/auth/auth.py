from flask import request
from flask_restx import Namespace, Resource

from project.container1 import users_service, auth_service

from project.setup.api.models import user

api = Namespace('auth')


@api.route('/register/')
class AuthView(Resource):
    def post(self):
        """
        Create new user
        :return:
        """
        data = request.json

        if data.get('email') and data.get('password'):
            users = users_service.create_user(data)
            return "OK", 200, {"location": f"/users/{users.id}"}
        else:
            return "Что то пошло не так", 401


@api.route('/login/')
class AuthView(Resource):
    def post(self):
        """
        Log in user
        """
        data = request.json

        email = data.get('email', None)
        password = data.get('password', None)

        if None in [email, password]:
            return '', 400

        tokens = auth_service.generate_token(email, password)

        return tokens, 201

    def put(self):  # создание новой пары токенов
        """
        Создание новой пары токенов
        :return:
        """
        data = request.json
        token = data.get('refresh_token')

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201
