import base64
import hashlib
import calendar
import datetime

import jwt
from flask import current_app, request
from flask_restx import abort

#from project.container1 import auth_service


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_password(password_hash, other_password):
    """

    :param password_hash:  пароль из БД
    :param other_password: пароль который прислал пользователь
    :return:
    """
    return password_hash == generate_password_hash(other_password)


def get_data_by_token(access_token):
    data = jwt.decode(access_token, key=current_app.config['SECRET_KEY'],
                      algorithms=current_app.config['ALGORITHM'])

    return data

def get_email_by_token(data):
    """
    Получение логина пользователя из валидного токена
    :param data:
    :return:
    """

    token = data['Authorization'].split('Bearer ')[-1]
    data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=current_app.config['JWT_ALGORITHM'])
    email = data['email']
    return email



def auth_required(func):
    """
    Декоратор проверки авторизации
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, key=current_app.config['SECRET_KEY'],
                       algorithms=current_app.config['JWT_ALGORITHM'])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper
