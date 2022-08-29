from flask import request
from flask_restx import Namespace, Resource

from project.container1 import users_service
from project.setup.api.models import user
from project.tools.security import auth_required, get_email_by_token


api = Namespace('user')

@api.route('/')
class UserView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    @auth_required
    def get(self):
        """
        get user
        :return:
        """
        email = get_email_by_token(request.headers)

        return users_service.get_by_email(email)

    @api.marshal_with(user, as_list=True, code=200, description='OK')
    @auth_required
    def patch(self):
        token = request.headers["Authorization"].split("Bearer ")[-1]
        data = request.json
        email = get_email_by_token(request.headers)
        return users_service.update_user(email, data)


@api.route('/password/')
class LoginView(Resource):
    @auth_required
    def put(self):
        """
        update token user
        """
        data = request.json
        token = request.headers["Authorization"].split("Bearer ")[-1]

        return users_service.update_password(data=data, token=token)


