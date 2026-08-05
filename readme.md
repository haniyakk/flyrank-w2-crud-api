# Task API — CRUD To-Do List

A small in-memory REST API for managing a to-do list, built with FastAPI as part of the FlyRank Internship Backend Track (Week 2, Assignment A1). Supports full CRUD — create, read, update, delete — on tasks, with interactive documentation via Swagger UI.

Data lives in memory only (no database) — it resets every time the server restarts.

## How to install & run

```
git clone https://github.com/haniyakk/flyrank-w2-crud-api.git
cd flyrank-w2-crud-api
python -m venv venv
venv\Scripts\Activate.ps1   # Windows PowerShell — use `source venv/bin/activate` on Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

The server runs on `http://127.0.0.1:8000`. Interactive docs are available at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| GET | `/` | API description | 200 | — |
| GET | `/health` | Health check | 200 | — |
| GET | `/tasks` | List all tasks | 200 | — |
| GET | `/tasks/{id}` | Get a single task | 200 | 404 if not found |
| POST | `/tasks` | Create a new task | 201 | 400 if title missing/empty |
| PUT | `/tasks/{id}` | Update a task's title and/or done status | 200 | 400 if title empty, 404 if not found |
| DELETE | `/tasks/{id}` | Delete a task | 204 | 404 if not found |

## Example — curl

```
curl -i http://127.0.0.1:8000/tasks
```

```
HTTP/1.1 200 OK
date: Wed, 05 Aug 2026 07:47:59 GMT
server: uvicorn
content-length: 127
content-type: application/json

[{"id":1,"title":"Workout","done":false},{"id":2,"title":"Read a book","done":true},{"id":3,"title":"Write code","done":false}]
```

## Swagger UI

![Swagger UI - endpoint list](swaggerSS1.png)

![Swagger UI - Try it out](swaggerSS2.png)

## Notes

- Data is stored in memory only — restarting the server resets tasks back to the 3 seed examples. This is intentional for this stage of the assignment (no database yet).