from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# TODO'ları tutacak liste
TODOS = []


class TodoSchema(BaseModel):
    id: int
    title: str  # 'tilt' yerine 'title' olarak düzeltilmiştir.
    is_important: Optional[bool]

    @classmethod
    def get_todos(cls):
        return TODOS

    @classmethod
    def add_todo(cls, todo):
        old_todo = next(filter(lambda x: x.id == todo.id, TODOS), None)
        if old_todo:
            return {'message': f'{todo.id}\'li todo mevcut olduğundan eklenemedi'}
        else:
            TODOS.append(todo)
            return {'message': 'TODO başarıyla eklendi.', "todo": todo}

    @classmethod
    def get_todo_by_id(cls, id):
        todo = next(filter(lambda x: x.id == id, TODOS), None)
        if todo:
            return {'todo': todo}
        else:
            return {'message': f'{id} id\'li todo bulunamadı'}

    @classmethod
    def remove_todo(cls, id):
        global TODOS
        todo = next(filter(lambda x: x.id == id, TODOS), None)
        if todo:
            TODOS = list(filter(lambda x: x.id != id, TODOS))
            return {'message': 'Todo silindi', 'todos': TODOS}
        else:
            return {'message': f'{id} id\'li todo bulunamadı'}

    @classmethod
    def update_todo(cls, id, todo):
        old_todo = next(filter(lambda x: x.id == id, TODOS), None)
        if old_todo:
            cls.remove_todo(old_todo.id)
            cls.add_todo(todo)
            return {'message': 'todo başarıyla güncellendi', 'yeni todo': todo}
        else:
            return {'message': f'{id} id\'li todo bulunamadı'}


@app.get('/todos/')
async def get_todos():
    return {'todos': TodoSchema.get_todos()}


@app.post('/todos/')
async def add_todo(todo: TodoSchema):
    return TodoSchema.add_todo(todo)


@app.get('/todos/{id}')
async def get_todo(id: int):
    return TodoSchema.get_todo_by_id(id)


@app.delete('/todos/{id}')
async def remove_todo(id: int):
    return TodoSchema.remove_todo(id)


@app.put('/todos/{id}')
async def update_todo(id: int, todo: TodoSchema):
    return TodoSchema.update_todo(id, todo)
