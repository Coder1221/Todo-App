import psycopg2
from models.todo import model
from typing import List
import abc
from abc import abstractmethod
from psycopg2.extras import DictRow, DictCursor


class AbstractTodoRepository(abc.ABC):
    @abstractmethod
    def add(self, todo: model.Todo):
        raise NotImplementedError

    def get_by_id(self, todo_id: str):
        raise NotImplementedError

    def delete(self, todo: model.Todo):
        raise NotImplementedError

    def save(self, todo: model.Todo):
        raise NotImplementedError


class TodoRepository(AbstractTodoRepository):
    def __init__(self, db_pool):
        super().__init__()
        #  a dbpool is a cache of database connections
        self.db_pool = db_pool

    def cursor(self, *args, **kwargs):
        return self.db_pool.cursor(*args, **kwargs)

    def read_cursor(self):
        # passing cursor factory as dictcursor which will return resuls in dict
        return self.cursor(cursor_factory=DictCursor)

    def get_by_id(self, todo_id: str) -> model.Todo:
        sql = """
            select * from todo_lists where id = %s;
        """
        with self.read_cursor() as curs:
            curs.execute(sql, [todo_id])
            todo_row = curs.fetchone()

        if todo_row:
            todo = _dict_row_to_todo(todo_row)
            return todo

    def add(self, todo: model.Todo):
        sql = """
            INSERT INTO todo_lists (
                id,
                user_id, 
                title, 
                description,
                status,
                priority,
                status_changed_on,
                created_at,
                updated_at
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """
        args = [
            todo.id,
            todo.user_id,
            todo.title,
            todo.description,
            todo.status,
            todo.priority,
            todo.status_changed_on,
            todo.created_at,
            todo.updated_at,
        ]
        with self.cursor() as curs:
            curs.execute(sql, args)

    def delete(self, todo: model.Todo):
        sql = """
            DELETE FROM todo_lists WHERE id =%s;
        """
        with self.cursor() as curs:
            curs.execute(sql, [todo.id])

    def save(self, todo: model.Todo) -> bool:
        sql = """
            UPDATE todo_lists
            SET 
                title = %s,
                description = %s,
                status = %s,
                priority = %s,
                status_changed_on = %s,
                updated_at = %s
            where id = %s
        """
        with self.read_cursor() as curs:
            curs.execute(
                sql,
                [
                    todo.title,
                    todo.description,
                    todo.status,
                    todo.priority,
                    todo.status_changed_on,
                    todo.updated_at,
                    todo.id,
                ],
            )
            success = bool(curs.fetchone())
        if not success:
            raise Exception("Record Not updated")

    def get_by_user_id_and_date(self, user_id: str, date: str):
        sql = """
            SELECT * from todo_lists where user_id = %s AND created_at::date = %s order by priority desc;
        """

        with self.read_cursor() as curs:
            curs.execute(sql, [user_id, date])
            res = curs.fetchall()
        if res:
            return list(map(_dict_row_to_todo, res))

        raise Exception("Data Not found")


def _dict_row_to_todo(r: DictRow) -> model.Todo:
    model_ = model.Todo(
        user_id=r["user_id"],
        title=r["title"],
        description=r["description"],
        status=r["status"],
    )
    model_.priority = r["priority"]
    model_.created_at = r["created_at"]
    model_.updated_at = r["updated_at"]
    model_.status_changed_on = r["status_changed_on"]
    return model_
