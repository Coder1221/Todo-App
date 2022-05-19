import psycopg2
from models.user import model
import abc
from typing import List
from psycopg2.extras import DictCursor, DictRow


class AbstractUserRepository(abc.ABC):
    def __init__(self):
        self.seen: List[model.User] = []

    def get_by_id(self, user_id: str):
        user = self._get_by_id(user_id)
        if user:
            self.seen.append(user)
        return user

    def add(self, user: model.User):
        self._add(user)
        self.seen.append(user)

    def save(self, user: model.User):
        self._save(user)
        self.seen.append(user)

    def delete(self, user: model.User):
        self._delete(user)
        self.seen.append(user)

    @abc.abstractmethod
    def _get_by_id(self, user_id: str):
        raise NotImplementedError

    def _add(self, user: model.User):
        raise NotImplementedError

    def _save(self, user: model.User):
        raise NotImplementedError

    def _delete(self, user: model.User):
        raise NotImplementedError


class UserRepository(AbstractUserRepository):
    def __init__(self, db_pool):
        super().__init__()
        self.db_pool = db_pool

    def cursor(self, *args, **kwargs):
        return self.db_pool.cursor(*args, **kwargs)

    def read_cursor(self):
        return self.cursor(cursor_factory=DictCursor)

    def _get_by_id(self, user_id: str):
        sql = """
            select * from users where id = %s;
        """
        with self.read_cursor() as curs:
            curs.execute(sql, [user_id])
            user_row = curs.fetchone()
        if user_row:
            user = _dict_row_to_user(user_row)
            return user

    def _add(self, user: model.User):
        sql = """
            INSERT INTO users(
                name,
                email,
                password
            )
            VALUES(
                %s,
                %s.
                %s
            )
        """

        args = [user.name, user.email, user.password]
        with self.read_cursor() as curs:
            curs.execute(sql, args)

    def _delete(self, user: model.User):
        sql = """
            DELETE FROM users WHERE id = %s
        """
        with self.read_cursor() as curs:
            curs.execute(sql, [user.id])

    def _save(self, user: model.User) -> bool:
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
    return model.User(
        id=user_row["id"],
        name=user_row["name"],
        email=user_row["email"],
        password=user_row["encrypted_password"],
    )
