from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    title: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
app = FastAPI()


tasks = [
    {"id": 1, "title": "Workout", "done": False},
    {"id": 2, "title": "Read a book", "done": True},
    {"id": 3, "title": "Write code", "done": False}
]

@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK, summary="Find and update a task by ID")
async def update_task(task_id: int, updated_task: TaskUpdate):
    for task in tasks: 
        if task["id"] == task_id:
            if updated_task.title is not None: 
                if not updated_task.title.strip():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Title can't be empty"
                    )
                task["title"] = updated_task.title
            
            if updated_task.done is not None: 
                task["done"] = updated_task.done
            
            return task

    raise  HTTPException( 
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Find and delete a task by ID")
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found"
    )

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a new task")
async def create_task(new_task: Task):
    if not new_task.title or new_task.title is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required and can't be empty"
        )
    task = {"id": max(t["id"] for t in tasks) + 1, "title": new_task.title, "done": False}
    tasks.append(task)
    return task

@app.get("/tasks", summary="Returns all tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", summary="Search task by ID")
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task {task_id} not found"
    )
    
@app.get("/", summary ="API Information")
async def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health", summary="API Health Check")
async def health_check():
	return {"status": "ok" }


'''
Stage 5 — See it: Swagger UI (~1–1.5 h)
So far you've imagined your API. Now look at it.

Swagger UI is a web page that reads a description of your API (an OpenAPI file) and turns it into interactive documentation: every endpoint listed, with a Try it out button that sends real requests — curl with a friendly face.

🐍 Python lane: open http://localhost:8000/docs . It's already there — FastAPI generates it from your code. Add a one-line description to each endpoint (see First steps(opens in a new tab) ) and watch the page improve.

🟨 JavaScript lane: install swagger-ui-express , write a small openapi.json describing your five task endpoints (the package README(opens in a new tab) shows the wiring; OpenAPI basic structure(opens in a new tab) explains the file). Serve it at /docs . Describing endpoints you already built teaches you more than building them did.

Then, in Swagger UI, without curl: create a task, list tasks, update it, delete it.

Checkpoint: /docs shows all your endpoints; "Try it out" works for the full CRUD cycle. Take a screenshot for your README.

Commit: Stage 5: Swagger UI

Stage 6 — Publish to GitHub (~1 h)
Your work only counts when someone else can run it.

Create a public GitHub repo and push your code (your ≥6 stage commits come with it).

Write a README with: what this is, how to install & run it (one documented command), a table of all endpoints, one pasted curl -i output, and your Swagger screenshot.

🗓️ New to Git? The basics are all you need here: init → add → commit → push — see the W2 resources, §9. And don't worry: next week's live session covers Git & GitHub properly — branches, pull requests, and how teams review work.

Checkpoint: a stranger with your README could run your API in under 5 minutes.

Commit: Stage 6: publish and docs — then push everything.

★ Make it yours — optional extras
No database yet — so let's have fun with what memory can do.

None of these are required. Pick whatever sounds fun (creative alternatives welcome):

Filtering with query parameters: GET /tasks?done=true returns only finished tasks. A query parameter is the part after ? — filters, not addresses.

Search: GET /tasks?search=milk returns tasks whose title contains the word.

A stats endpoint: GET /stats → { "total": 7, "done": 3, "open": 4 } — your first taste of the server computing something instead of just storing it.

Seed & reset: POST /reset restores the 3 example tasks. Handy for demos — and for the next point.

The mortality experiment: create a few tasks, restart your server, GET /tasks . Write two sentences in your README about what happened and why. This observation is the entire reason Week 3 exists.

Commit (if you build any): Extras: <what you added>

Stage 7 — Bonus: the AI rematch (~1 h, optional — and the most fun)
You built this API by hand, line by line. Now hire the fastest junior developer on Earth — and review their work.

You did Stages 0–6 by hand for a reason: you now know exactly what "correct" looks like. That knowledge is what turns this stage from a magic show into a code review.

Write the prompt yourself — this is the real exercise. Without copying text from this document, write your own prompt asking an AI assistant (Claude, ChatGPT, Gemini — any) to build the same API. From memory, try to specify everything that matters: language and framework, the five endpoints, status codes, validation rules, in-memory storage, Swagger UI. Describing a system precisely is a core backend skill — you'll meet it again in Week 7's spec-first build.

Generate in quarantine. Put the AI's code in a separate folder ( ai-version/ ) or a branch. Your Stages 0–6 code stays untouched — that is your hand-built submission, and it must stay hand-built.

Run it. Does it start on the first try? Fire your Stage 4 checkpoint curls at it. Which pass? Which fail?

Diff it. Compare the AI's code with yours side by side ( git diff --no-index your-file ai-file works on any two files). Then answer three questions in a short "AI vs me" section of your README:

What did the AI do better — and do you understand its version well enough to explain it?

What did it get wrong or quietly ignore from your prompt? (A missing 400 ? A wrong status code? A database you never asked for?)

What did your prompt forget to specify — and what did the AI silently decide for you?

One rematch. Improve your prompt with what you learned, regenerate, and note in one sentence what changed.
The lesson hiding in this stage: an AI's output is exactly as good as your specification — and you could only judge it because you had built the thing yourself first. Both halves of that sentence are your career from now on.

Checkpoint: your README has an "AI vs me" section containing your full prompt and at least three concrete differences you found.

Commit: Stage 7: AI vs me (AI code stays in its own folder/branch).
'''