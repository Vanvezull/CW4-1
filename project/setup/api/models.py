from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия')
})

director: Model = api.model('Режиссеры', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия')
})

movie: Model = api.model('Фильмы', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Комедия'),
    'description': fields.String(required=True, max_length=100, example='Комедия'),
    'trailer': fields.String(required=True, max_length=100, example='Комедия'),
    'year': fields.Integer(required=True, max_length=100, example='Комедия'),
    'rating': fields.Float(required=True, max_length=100, example='Комедия'),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director)
})

user: Model = api.model('Пользователи', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'name': fields.String(required=True),
    'surname': fields.String(required=True),
    'favourite_genre': fields.Integer(),
    'genre': fields.Nested(genre),
})
