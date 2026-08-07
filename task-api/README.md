# Task API (in-memory CRUD)

## Run
```
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

## Endpoints
- GET    /            - API description
- GET    /health       - health check
- GET    /tasks        - list all tasks
- GET    /tasks/{id}   - get one task
- POST   /tasks        - create a task (title required)
- PUT    /tasks/{id}   - update a task (title and/or done)
- DELETE /tasks/{id}   - delete a task
