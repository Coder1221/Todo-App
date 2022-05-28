import psycopg2
from repository import todo_repository, user_repository
from models.todo import model as td
from models.user import model as tu

if __name__ == "__main__":
    conn = psycopg2.connect(
        host="localhost", database="todo", user="abdurrehmansajid", password="luminite"
    )
    repo = todo_repository.TodoRepository(conn)
    # repo2 = user_repository.UserRepository(conn)
    # a = repo2.get_by_id('90327d11-78cd-418a-b443-c5aab627088b')
    # print(a)
    # model  = td.Todo(user_id= a.id ,title="new_title" ,description="DESCRIPTION",status="IN_PROGRESS")

    # print(model)
    # repo.add(model)
    # conn.commit()

    todo = repo.get_by_id("f1b1cec5-536a-4c19-a0ea-f623baad31d0")
    print(todo)
    # repo.delete(todo)
    # conn.commit()
