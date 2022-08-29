from project.dao.main import UsersDAO
from project.tools.security import generate_password_hash, get_data_by_token


# from project.tools.security import generate_password_hash


class UsersService:
    def __init__(self, dao: UsersDAO):
        self.dao = dao

    def get_one(self, uid):
        """
        Сервис получения одного пользователя
        :param uid:
        :return:
        """
        return self.dao.get_by_id(uid)

    def get_by_email(self, email):
        """
        Сервис поиска пользователя по логину (email)
        :param email:
        :return:
        """
        return self.dao.get_user_by_email(email)

    def get_all(self):
        """
        Сервис получения всех пользователей
        :return:
        """
        users = self.dao.get_all()
        return users

    def create_user(self, user_d):
        """
        Сервис создания пользователя
        :param user_d:
        :return:
        """
        user_d['password'] = generate_password_hash(user_d['password'])
        return self.dao.create_user(user_d)

    def update_user(self, email, user_d):
        """
        Сервис обновления данных о пользователе
        :param user_d:
        :return:
        """
        # user_d['email'] = generate_password_hash(user_d['email'])

        return self.dao.update_user(email, user_d)

    def update_password(self, email, new_password):
        """
        Сервис обновления пароля пользователя
        :param user_d:
        :param new_password:
        :return:
        """
        self.dao.update_password(email, new_password)

    # def delete(self, uid):
    #     """
    #     Сервис удаления пользователя
    #     :param uid:
    #     :return:
    #     """
    #     self.dao.delete(uid)

    def get_user_by_token(self, token):
        data = get_data_by_token(token)
        return self.get_by_email(data.get('email'))
