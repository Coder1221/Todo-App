from dataclasses import dataclass
from datetime import date, datetime
import time
from .status_enum import Status
from typing import List
import uuid


@dataclass
class Todo:
    id: str
    user_id: str
    title: str
    description: str
    status: int
    priority: int
    status_changed_on: datetime
    created_at: datetime
    updated_at: datetime

    def __init__(self, user_id, title, description, status):
        self.id = str(uuid.uuid1())
        self.user_id = user_id
        self.title = title
        self.description = description
        self.status = status
        self.priority = 0
        self.status_changed_on = None
        self.created_at = datetime.now()
        self.updated_at = None

    def update_status(self, status) -> None:

        """raising keyerror in case if we don't have the key in status enum"""
        if status not in Status.__members__:
            raise KeyError("Status {} is not valid".format(status))

        """Checking if the status provided is same as the current status"""
        if Status(self.status).value == Status[status].value:
            raise Exception("Status is already {}".format(status))

        self.status = Status[status].value
        self.status_changed_on = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    def update_title(self, title) -> bool:
        self.title = title
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        return True

    def update_description(self, description) -> bool:
        self.description = description
        self.updated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        return True

    def increase_priority(self):
        self.priority = self.priority + 1

    def decrease_priority(self):
        self.priority = self.priority - 1


class ListTodo:
    def __init__(self, todo_repository):
        self.repository = todo_repository

    def get_by_user_id_and_date(self, user_id: str, date: str) -> List[Todo]:
        """Returns a list todo of certain date"""
        return self.repository.get_by_user_id_and_date(user_id, date)

    def sort_by_priority(self, todos: List[Todo]) -> List[Todo]:
        """ "Will sort a list of todos based on the priority (highest number means highest priority)"""
        """Also returns the dict of priority count"""
        raise NotImplementedError

    def increase_priority(self, todo_id: str, date: str):
        """Increments the priority of of the given todo"""
        todo = self.repository.get(todo_id)
        todos = self.repository.get_by_user_id_and_date(todo.user_id, date)
        sorted_todos, dict_priority_count = self.sort_by_priority(todos)

        # in the dict find the key with the max_value
        max_priority = -1
        for key in dict_priority_count:
            if key > max_priority:
                max_priority = key

        if todo.priority < max_priority or (
            todo.priority == max_priority and dict_priority_count[max_priority] > 1
        ):
            todo.increase_priority()
            self.repository.save(todo)
        else:
            raise Exception("Already on the highest priority")

    def decrease_priority(self, todo_id: str, date: str):
        """Increments the priority of of the given todo"""
        todo = self.repository.get(todo_id)
        if todo.priority > 0:
            todo.decrease_priority()
            self.repository.save(todo)
        else:
            raise Exception("Already on the lowest priority")
