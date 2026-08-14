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
    if new_task.title is not None and not new_task.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title can't be empty"
        )
    curr_id =  max(t["id"] for t in tasks) + 1
    task = {"id": curr_id + 1, "title": new_task.title, "done": False}
    tasks.append(task)
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    sql_query = " INSERT INTO tasks (id, title, done) VALUES (?, ?, False)"
    cursor.execute(sql_query, (curr_id, new_task.title, ))
    conn.commit()
    conn.close()
    return task


@app.get("/tasks", summary="Returns all tasks")
async def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(" SELECT * FROM tasks ")
    results = cursor.fetchall()
    if results != None:
        for r in results: 
            print(r)
    conn.close()
    
    return results
'''
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
'''



@app.get("/tasks/{task_id}", summary="Search task by ID")
async def get_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    sql_query = " SELECT * FROM tasks WHERE id = ?"
    cursor.execute(sql_query, (task_id,))
    result = cursor.fetchone()
    if result != None:
        return result
        conn.close()

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
