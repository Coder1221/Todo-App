from services.todo.adapters import repository
import services.todo.domain.model as model
from typing import List, Dict, Tuple
import backend.services.exceptions as errors


def create_todo(
    user_id: str,
    title: str,
    description: str,
    status: str,
    repo: repository.AbstractTodoRepository,
) -> None:
    """Create a new todo"""
    todo = model.Todo(
        user_id=user_id, title=title, description=description, status=status
    )
    repo.add(todo)


def increase_priority(
    todo_id: str, user_id: str, repo: repository.AbstractTodoRepository
) -> None:
    """Increments the priority of of the given todo"""
    todo = repo.get_by_id(todo_id)

    if not todo:
        raise errors.TodoNotFound("Todo not found")

    todo_created_date = todo.created_at.strftime("%Y-%m-%d")

    todos_by_created_date = repo.get_by_user_id_and_date_by_priority(
        todo.user_id, todo_created_date
    )

    dict_priority_count = _priority_dict_count(todos_by_created_date)

    max_priority = _max_priority(todos_by_created_date)

    # if Max priority of todos is less than  the given todo priority or 
    # given todo priority is equal to max priority and count of max_priority is greter than one
    # then we will increase the priority

    if todo.priority < max_priority or (
        todo.priority == max_priority and dict_priority_count[max_priority] > 1
    ):
        todo.increase_priority()
        repo.save(todo)
    else:
        raise errors.AlreadyOnHighestPriority("Already on the highest priority")


def decrease_priority(
    todo_id: str, user_id: str, repo: repository.AbstractTodoRepository
) -> None:
    """Decrements the priority of of the given todo"""
    todo = repo.get_by_id(todo_id)

    if not todo:
        raise errors.TodoNotFound("Todo not found")

    if todo.priority > 0:
        todo.decrease_priority()
        repo.save(todo)
    else:
        raise errors.AlreadyOnLowPriority("Already on the lowest priority")


def _max_priority(self, todos: List[model.Todo]) -> int:
    """Returns the maximum priority for a given list of todos"""
    max_priority = -1
    for todo in todos:
        if todo.priority > max_priority:
            max_priority = todo.priority
    return max_priority


def _priority_dict_count(self, todos: List[model.Todo]) -> Dict:
    """Returns the dict of priority count where key is the priority and value is the number of times that priority appeared"""
    dict_ = {}
    for todo in todos:
        try:
            dict_[todo.priority] = dict_[todo.priority] + 1
        except KeyError as e:
            dict_[todo.priority] = 1
    return dict_
