import calendar
import datetime

import jwt
from flask import current_app

from flask_restx import abort

from project.config import BaseConfig
from project.services.users_service import UsersService
from project.tools.security import compare_password


class AuthService:

    def __init__(self, user_service: UsersService):
        self.user_service = user_service

    def generate_token(self, email, password, is_refresh=False):
        """
        Функция создания access_token и refresh_token
        """
        user = self.user_service.get_by_email(email)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not compare_password(user.password, password):
                abort(400)

        data = {
            'email': user.email,
        }

        # 30 minutes for access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, key=current_app.config["SECRET_KEY"],
                                  algorithm=current_app.config["JWT_ALGORITHM"])

        # 130 days for refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, key=current_app.config["SECRET_KEY"],
                                   algorithm=current_app.config["JWT_ALGORITHM"])

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        """
        Функция создания новой пары access_token и refresh_token по refresh_token
        :param refresh_token:
        :return:
        """
        data = jwt.decode(jwt=refresh_token, key=current_app.config["SECRET_KEY"],
                          algorithms=current_app.config["JWT_ALGORITHM"])
        email = data.get('email')

        return self.generate_token(email, None, is_refresh=True)
