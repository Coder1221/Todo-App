import psycopg2
import backend.services.user.domain.model as model
import abc
from typing import List, Dict
from psycopg2.extras import DictCursor, DictRow
from backend.services.exceptions import RecordNotUpdated

# took inspiration from https://github.com/tajir-app/tajir/blob/master/ddd-template/services/catalog/adapters/repository.py


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, user_id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str):
        raise NotImplementedError


class UserRepository(AbstractUserRepository):
    def __init__(self, db_pool):
        super().__init__()
        self.db_pool = db_pool

    def cursor(self, *args, **kwargs):
        return self.db_pool.cursor(*args, **kwargs)

    def read_cursor(self):
        return self.cursor(cursor_factory=DictCursor)

    def get_by_id(self, user_id: str):
        sql = """
            select * from users where id = %s and deleted = false;
        """
        with self.read_cursor() as curs:
            curs.execute(sql, [user_id])
            user_row = curs.fetchone()
        if user_row:
            user = _dict_row_to_user(user_row)
            return user

    def add(self, user: model.User):
        sql = """
            insert into users(
                id,
                name,
                email,
                encrypted_password
            )
            values(
                %s,
                %s,
                %s,
                %s
            )
        """

        args = [user.id, user.name, user.email, user.password]
        with self.read_cursor() as curs:
            curs.execute(sql, args)

    def delete(self, user: model.User):
        sql = """
            update users
            set
                deleted = True
            where id = %s
        """
        with self.read_cursor() as curs:
            curs.execute(sql, [user.id])

    def save(self, user: model.User) -> bool:
        sql = """
            update users 
            set 
                name = %s, 
                email = %s,
                encrypted_password = %s
            where id = %s
            returning id;
        """
        args = [user.name, user.email, user.password, user.id]
        with self.read_cursor() as curs:
            curs.execute(sql, args)
            success = bool(curs.fetchone())

        if not success:
            raise RecordNotUpdated("Record not updated")

    def get_by_email(self, email: str) -> model.User:
        sql = """
            select * from users where email = %s;
        """
        with self.read_cursor() as cursor:
            cursor.execute(sql, [email])
            user_row = cursor.fetchone()
        if user_row:
            return _dict_row_to_user(user_row)


class FakeUserRepository(AbstractUserRepository):
    def __init__(self):
        super().__init__()
        self.users: Dict[str, model.User] = {}

    def get_by_id(self, user_id: str):
        return self.users.get(user_id, None)

    def add(self, user: model.User):
        self.users[user.id] = user

    def save(self, user: model.User):
        self.users[user.id] = user

    def delete(self, user: model.User):
        self.users.pop(user.id, None)

    def get_by_email(self, email: str):
        for i in self.users.values():
            if i.email == email:
                return self.users[i.id]
        return None


def _dict_row_to_user(user_row: DictRow) -> model.User:
    return model.User(
        id=user_row["id"],
        name=user_row["name"],
        email=user_row["email"],
        password=user_row["encrypted_password"],
    )
