from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from models import TaskCreate, TaskUpdate

app = FastAPI(title="Task", version="1.0")

class AppError(Exception):
    """App-level error, independent of FastAPI's built-in HTTPException/detail shape."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})

# In-memory storage: dict keyed by id for O(1) lookup/update/delete
tasks: dict[int, dict] = {}
next_id = 1

def _title_is_blank(title) -> bool:
    return title is None or title.strip() == ""


@app.get("/")
def read_root():
    return {"name": "Task", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_all_tasks():
    return list(tasks.values())

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        raise AppError(404, f"Task {task_id} not found")
    return task

@app.post("/tasks", status_code=201)
def create_task(task_in: TaskCreate):
    global next_id

    if _title_is_blank(task_in.title):
        raise AppError(400, "Title can't be empty")

    new_task = {"id": next_id, "title": task_in.title, "done": False}
    tasks[next_id] = new_task
    next_id += 1
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_in: TaskUpdate):
    task = tasks.get(task_id)
    if task is None:
        raise AppError(404, f"Task {task_id} not found")

    if task_in.title is not None:
        if _title_is_blank(task_in.title):
            raise AppError(400, "Title can't be empty")
        task["title"] = task_in.title

    if task_in.done is not None:
        task["done"] = task_in.done

    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise AppError(404, f"Task {task_id} not found")
    del tasks[task_id]
    return Response(status_code=204)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)