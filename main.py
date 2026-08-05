from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    title: Optional[str] = None

app = FastAPI()


tasks = [
    {"id": 1, "title": "Workout", "done": False},
    {"id": 2, "title": "Read a book", "done": True},
    {"id": 3, "title": "Write code", "done": False}
]

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(new_task: Task):
    if not new_task.title or new_task.title is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required and can't be empty"
        )
    task = {"id": max(t["id"] for t in tasks) + 1, "title": new_task.title, "done": False}
    tasks.append(task)
    return task

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task {task_id} not found"
    )
    
@app.get("/")
async def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health_check():
	return {"status": "ok" }


'''
Stage 3 — Create: POST a new task (~1 h)
A customer walks in with a new order.

Add POST /tasks . The client sends the new task as JSON in the request body :
{ "title": "Buy milk" }

Your server: gives it the next free id , sets done to false , adds it to the list, and returns the created task with status 201 ("Created" — the polite way to say "done, here's your receipt").

Validate the input: if title is missing or empty, return 400 ("Bad Request") with a JSON error saying what's wrong. This is your first business rule — the server never trusts the client.

Checkpoint:

curl -i -X POST [http://localhost:3000/tasks](http://localhost:3000/tasks) -H "Content-Type: application/json" -d '{"title":"Buy milk"}'

returns 201 + the new task, and a second GET /tasks shows it in the list. Posting {} returns 400.

Commit: Stage 3: create with validation


just adding into the comment hehehe
'''