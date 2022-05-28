from repository.todo_repository import TodoRepository
from model import Todo
from typing import List, Dict
import services.exceptions as errors


class ListTodo:
    """This model is not saving any it is for interacting with db layer"""

    def __init__(self, todo_repository: TodoRepository):
        self.repository = todo_repository

    def get_by_user_id_and_date_by_priority_(
        self, user_id: str, date: str
    ) -> List[Todo]:
        """Returns a list todo of certain date order by priority"""
        return self.repository.get_by_user_id_and_date_by_priority(user_id, date)

    def _priority_dict_count(self, todos: List[Todo]) -> Dict:
        """Returns the dict of priority count where key is the priority and value is the number of times that priority appeared"""
        dict_ = {}
        for todo in todos:
            try:
                dict_[todo.priority] = dict_[todo.priority] + 1
            except KeyError as e:
                dict_[todo.priority] = 1
        return dict_

    def _max_priority(self, todos: List[Todo]) -> int:
        """Returns the maximum priority for a given list of todos"""
        max_priority = -1
        for todo in todos:
            if todo.priority > max_priority:
                max_priority = todo.priority
        return max_priority

    def increase_priority(self, todo_id: str, user_id: str) -> None:
        """Increments the priority of of the given todo"""
        todo = self.repository.get_by_id(todo_id)
        if not todo:
            raise errors.TodoNotFound("Todo not found")

        # if todo.user_id != user_id:
        #     raise errors.UnAuthorized("Not authorized")

        todo_created_date = todo.created_at.strftime("%Y-%m-%d")

        todos_by_created_date = self.repository.get_by_user_id_and_date_by_priority(
            todo.user_id, todo_created_date
        )

        dict_priority_count = self._priority_dict_count(todos_by_created_date)

        max_priority = self._max_priority(todos_by_created_date)

        #  if max_priority is less than todo priority or todo priority is equal to max_priority and count of max_priority is greter than one
        # then increase_priority else raise exception

        if todo.priority < max_priority or (
            todo.priority == max_priority and dict_priority_count[max_priority] > 1
        ):
            todo.increase_priority()
            self.repository.save(todo)
        else:
            raise errors.AlreadyOnHighestPriority("Already on the highest priority")

    def decrease_priority(self, todo_id: str, user_id: str) -> None:
        """Decrements the priority of the given todo"""
        todo = self.repository.get_by_id(todo_id)
        if todo.priority > 0:
            todo.decrease_priority()
            self.repository.save(todo)
        else:
            raise errors.AlreadyOnLowPriority("Already on the lowest priority")
