from services.todo.adapters import repository
import services.todo.domain.model as model
from typing import List ,  Dict

def create_todo(
    user_id: str,
    title: str,
    description: str,
    status: str,
    repo: repository.AbstractTodoRepository,
):

    todo = model.Todo(
        user_id=user_id, title=title, description=description, status=status
    )

    saved_todo = repo.add(todo)

    return {
        "success": True,
        "message": "Todo created successfully",
        "data": saved_todo,
    }
    
def increase_priority(todo_id: str, user_id: str , repo: repository.AbstractTodoRepository):
    """Increments the priority of of the given todo"""
    todo = repo.get_by_id(todo_id)
    
    if not todo:
        raise Exception("Todo not found")
    
    created_date = todo.created_at.strftime("%Y-%m-%d")

    all_todos = repo.get_by_user_id_and_date_by_priority(todo.user_id, created_date)

    dict_priority_count, max_priority = _priority_dict_count(all_todos)

    if todo.priority < max_priority or (
        todo.priority == max_priority and dict_priority_count[max_priority] > 1
    ):
        todo.increase_priority()
        repo.save(todo)
    else:
        raise Exception("Already on the highest priority")
   
def decrease_priority(todo_id: str, user_id: str  ,repo: repository.AbstractTodoRepository):
    """Decrements the priority of of the given todo"""
    todo = repo.get_by_id(todo_id)

    if todo.priority > 0:
        todo.decrease_priority()
        repo.save(todo)
    else:
        raise Exception("Already on the lowest priority")


def _priority_dict_count(self, todos: List[model.Todo]) -> List[model.Todo]:
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

