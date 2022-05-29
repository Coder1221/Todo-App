import psycopg2
from services.todo.domain import model
from typing import List, Optional, Dict
import abc
from abc import abstractmethod
from psycopg2.extras import DictRow, DictCursor

# took inspiration from https://github.com/tajir-app/tajir/blob/master/ddd-template/services/catalog/adapters/repository.py


class AbstractTodoRepository(abc.ABC):
    @abstractmethod
    def add(self, todo: model.Todo):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, todo_id: str):
        raise NotImplementedError

    @abstractmethod
    def delete(self, todo: model.Todo):
        raise NotImplementedError

    @abstractmethod
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

    def get_by_id(self, todo_id: str) -> Optional[model.Todo]:
        sql = """
            select * from todo_lists where id = %s  and deleted = false;
        """
        with self.read_cursor() as curs:
            curs.execute(sql, [todo_id])
            todo_row = curs.fetchone()

        return _dict_row_to_todo(todo_row) if todo_row else None

    def add(self, todo: model.Todo):
        sql = """
            insert into todo_lists (
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
            values (
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
            update todo_lists 
            set
                deleted = True
            where id = %s
        """
        with self.cursor() as curs:
            curs.execute(sql, [todo.id])

    def save(self, todo: model.Todo):
        sql = """
            update todo_lists
            set 
                title = %s,
                description = %s,
                status = %s,
                priority = %s,
                status_changed_on = %s,
                updated_at = %s
            where id = %s
        """

        args = [
            todo.title,
            todo.description,
            todo.status,
            todo.priority,
            todo.status_changed_on,
            todo.updated_at,
            todo.id,
        ]
        with self.read_cursor() as curs:
            curs.execute(sql, args)

    def get_by_user_id_and_date_by_priority(
        self, user_id: str, date: str
    ) -> List[model.Todo]:
        """Will return a list of todos of users with on the given data sorted by priority"""

        sql = """
            select * from todo_lists where user_id = %s and created_at::date = %s order by priority desc;
        """

        with self.read_cursor() as curs:
            curs.execute(sql, [user_id, date])
            res = curs.fetchall()

        return [_dict_row_to_todo(todo) for todo in res] if res else None


class FakeTodoRepository(AbstractTodoRepository):
    """Fake TodoRepository for testing purposes"""

    def __init__(self):
        super().__init__()
        self.todos: Dict[str, model.Todo] = {}

    def add(self, model: model.Todo):
        self.todos[model.id] = model

    def save(self, model: model.Todo):
        self.todos[model.id] = model

    def get_by_id(self, todo_id: str) -> model.Todo:
        return self.todos.get(todo_id, None)

    def delete(self, model: model.Todo):
        self.todos.pop(model.id, None)


def _dict_row_to_todo(r: DictRow) -> model.Todo:
    return model.Todo(
        user_id=r["user_id"],
        title=r["title"],
        description=r["description"],
        status=r["status"],
        id=r["id"],
        priority=r["priority"],
        created_at=r["created_at"],
        updated_at=r["updated_at"],
        status_changed_on=r["status_changed_on"],
    )
