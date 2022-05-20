import psycopg2
from models.user import model
import abc
from typing import List
from psycopg2.extras import DictCursor, DictRow


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, user_id: str):
        raise NotImplementedError

    def add(self, user: model.User):
        raise NotImplementedError

    def save(self, user: model.User):
        raise NotImplementedError

    def delete(self, user: model.User):
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
            select * from users where id = %s;
        """
        with self.read_cursor() as curs:
            curs.execute(sql, [user_id])
            user_row = curs.fetchone()
        if user_row:
            user = _dict_row_to_user(user_row)
            return user

    def add(self, user: model.User):
        sql = """
            INSERT INTO users(
                id,
                name,
                email,
                encrypted_password
            )
            VALUES(
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
            DELETE FROM users WHERE id = %s
        """
        with self.read_cursor() as curs:
            curs.execute(sql, [user.id])

    def save(self, user: model.User) -> bool:
        sql = """
            UPDATE users 
            SET 
                name = %s, 
                email = %s,
                encrypted_password = %s
            where id = %s
            returning id;
        """
        args = [user.name, user.email, user.password, user.id]
        print(args)
        with self.read_cursor() as curs:
            curs.execute(sql, args)
            success = bool(curs.fetchone())

        if not success:
            raise Exception("Record not updated")


def _dict_row_to_user(user_row: DictRow) -> model.User:
    model_ = model.User(
        name=user_row["name"],
        email=user_row["email"],
        password=user_row["encrypted_password"],
    )
    model_.id = user_row["id"]
    return model_
