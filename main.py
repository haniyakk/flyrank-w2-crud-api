from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }


@app.get("/health")
async def health_check():
	return {"status": "ok" }


'''
Stage 1 — Your first real endpoint (~45 min)
Every API needs a front door that says what it is.

Add the endpoint GET / returning JSON that describes your API:
{ "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

Add GET /health returning { "status": "ok" } . Real companies use exactly this endpoint to check a server is alive — you've just built your first professional habit.
Checkpoint: both URLs return JSON in the browser and via curl.

Commit: Stage 1: root and health endpoints

Stage 2 — Read: list and single task (~1 h)
Now the shelves. Your "database" is just a list in your code.

Near the top of your file, create an in-memory list of task objects, pre-filled with 3 example tasks. Each task has: id (number), title (text), done (true/false).

Add GET /tasks — returns the whole list.

Add GET /tasks/:id (Express) / GET /tasks/{id} (FastAPI) — returns one task. The id part is a path parameter : a piece of the URL that changes.

If no task has that id, return status 404 with a JSON error: { "error": "Task 99 not found" } . Never return an empty 200 for something that doesn't exist — status codes are how machines read your answers.

Checkpoint: curl -i http://localhost:3000/tasks/1 → 200 + one task · curl -i http://localhost:3000/tasks/99 → 404 + error JSON.

Commit: Stage 2: read endpoints with 404
'''