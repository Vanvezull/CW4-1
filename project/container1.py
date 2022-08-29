from project.dao.main import GenresDAO, MoviesDAO, DirectorsDAO, UsersDAO


from project.services import GenresService, MoviesService, DirectorsService, UsersService
from project.services.auth_service import AuthService
from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
movie_dao = MoviesDAO(db.session)
director_dao = DirectorsDAO(db.session)
user_dao = UsersDAO(db.session)

# Services
genres_service = GenresService(dao=genre_dao)
movies_service = MoviesService(dao=movie_dao)
directors_service = DirectorsService(dao=director_dao)
users_service = UsersService(dao=user_dao)
auth_service = AuthService(users_service)
