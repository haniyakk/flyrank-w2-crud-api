from fastapi import FastAPI, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
import sqlite3

class Task(BaseModel):
    title: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

app = FastAPI()

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

def define_conn():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, done BOOLEAN)")
    conn.commit()
    conn.close()

def adding_hardcoded_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    sql_query = """ INSERT INTO tasks 
                (id, title, done) 
                VALUES
                (1, 'Cleaning Table', 'False'),
                (2, 'Doodle', 'False'),
                (3, 'Wash bottles', 'False') """
    define_conn()
    cursor.execute(sql_query)
    conn.commit()
    cursor.close()

@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK, summary="Find and update a task by ID")
async def update_task(task_id: int, updated_task: TaskUpdate):
    
    record = get_task(task_id) 
    idToBeUpdated = record["id"]
    
    if updated_task.title is not None and not updated_task.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty."
        )
 
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
 
    if updated_task.title is not None:
        sql_query = "UPDATE tasks SET title = ? WHERE id = ?"
        cursor.execute(sql_query, (updated_task.title, idToBeUpdated, ))
 
    if updated_task.done is not None:
        sql_query2 = "UPDATE tasks SET done = ? WHERE id = ?"
        cursor.execute(sql_query2, (updated_task.done, task_id, ))
 
    conn.commit()
    conn.close()
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Find and delete a task by ID")
async def delete_task(task_id: int):
    get_task(task_id)
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    sql_query = "DELETE FROM tasks WHERE id = ?"
    cursor.execute(sql_query, (task_id, ))
    conn.commit()
    conn.close()
    return

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a new task")
async def create_task(new_task: Task):
    
    if new_task.title is not None and not new_task.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title can't be empty"
        )
    
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    sql_query = " INSERT INTO tasks (title, done) VALUES (?, ?)"
    cursor.execute(sql_query, (new_task.title, False))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    task = {"id": new_id, "title": new_task.title, "done": False}
    return task

@app.get("/tasks", summary="Returns all tasks")
async def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(" SELECT * FROM tasks ")
    results = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "done": bool(r[2])} for r in results]

@app.get("/tasks/{task_id}", summary="Search task by ID")
def get_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    sql_query = " SELECT * FROM tasks WHERE id = ?"
    cursor.execute(sql_query, (task_id,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task {task_id} not found"
    )
    return {"id": result[0], "title": result[1], "done": bool(result[2])}
    
    
@app.get("/", summary ="API Information")
async def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health", summary="API Health Check")
async def health_check():
	return {"status": "ok" }
