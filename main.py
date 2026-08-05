from fastapi import FastAPI, HTTPException, status

app = FastAPI()


tasks = [
    {"id": 1, "title": "Workout", "done": False},
    {"id": 2, "title": "Read a book", "done": True},
    {"id": 3, "title": "Write code", "done": False}
]

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

Stage 2 — Read: list and single task (~1 h)
Now the shelves. Your "database" is just a list in your code.

Near the top of your file, create an in-memory list of task objects, pre-filled with 3 example tasks. Each task has: id (number), title (text), done (true/false).

Add GET /tasks — returns the whole list.

Add GET /tasks/:id (Express) / GET /tasks/{id} (FastAPI) — returns one task. The id part is a path parameter : a piece of the URL that changes.

If no task has that id, return status 404 with a JSON error: { "error": "Task 99 not found" } . Never return an empty 200 for something that doesn't exist — status codes are how machines read your answers.

Checkpoint: curl -i http://localhost:3000/tasks/1 → 200 + one task · curl -i http://localhost:3000/tasks/99 → 404 + error JSON.

Commit: Stage 2: read endpoints with 404

just adding into the comment hehehe
'''