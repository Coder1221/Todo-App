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

    def get_by_user_id_and_date_by_priority(
        self, user_id: str, date: str
    ) -> List[Todo]:
        """Returns a list todo of certain date order by priority"""
        return self.repository.get_by_user_id_and_date_by_priority(user_id, date)

    def priority_dict_count(self, todos: List[Todo]) -> List[Todo]:
        """Returns the dict of priority count and max_priority"""
        dict_ = {}
        max_priority = -1
        for todo in todos:
            try:
                if todo.priority > max_priority:
                    max_priority = todo.priority
                dict_[todo.priority] = dict_[todo.priority] + 1
            except:
                dict_[todo.priority] = 1
        return dict_, max_priority

    def increase_priority(self, todo_id: str):
        """Increments the priority of of the given todo"""
        todo = self.repository.get_by_id(todo_id)
        date = todo.created_at.strftime("%Y-%m-%d")

        todos = self.repository.get_by_user_id_and_date_by_priority(todo.user_id, date)
        dict_priority_count, max_priority = self.priority_dict_count(todos)

        if todo.priority < max_priority or (
            todo.priority == max_priority and dict_priority_count[max_priority] > 1
        ):
            todo.increase_priority()
            self.repository.save(todo)
        else:
            raise Exception("Already on the highest priority")

    def decrease_priority(self, todo_id: str):
        """Increments the priority of of the given todo"""
        todo = self.repository.get_by_id(todo_id)
        if todo.priority > 0:
            todo.decrease_priority()
            self.repository.save(todo)
        else:
            raise Exception("Already on the lowest priority")
