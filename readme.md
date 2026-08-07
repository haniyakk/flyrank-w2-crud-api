# Task API: CRUD To Do List

A small in memory REST API for managing a to do list, built with FastAPI as part of the FlyRank Internship Backend Track (Week 2, Assignment A1). It supports full CRUD operations: create, read, update, and delete tasks, with interactive documentation through Swagger UI.

Data is stored in memory only, so it resets every time the server restarts.

## How to install and run

```bash
git clone https://github.com/haniyakk/flyrank-w2-crud-api.git
cd flyrank-w2-crud-api
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

If you are using Mac or Linux, activate the virtual environment with:

```bash
source venv/bin/activate
```

The server runs at `http://127.0.0.1:8000`.

Interactive documentation is available at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Path          | Description                        | Success | Errors                                  |
| ------ | ------------- | ---------------------------------- | ------- | --------------------------------------- |
| GET    | `/`           | API description                    | 200     | None                                    |
| GET    | `/health`     | Health check                       | 200     | None                                    |
| GET    | `/tasks`      | List all tasks                     | 200     | None                                    |
| GET    | `/tasks/{id}` | Get a single task                  | 200     | 404 if not found                        |
| POST   | `/tasks`      | Create a new task                  | 201     | 400 if title is missing or empty        |
| PUT    | `/tasks/{id}` | Update a task title or done status | 200     | 400 if title is empty, 404 if not found |
| DELETE | `/tasks/{id}` | Delete a task                      | 204     | 404 if not found                        |

## Example using curl

```bash
curl -i http://127.0.0.1:8000/tasks
```

Example response:

```text
HTTP/1.1 200 OK
date: Wed, 05 Aug 2026 07:47:59 GMT
server: uvicorn
content-length: 127
content-type: application/json

[{"id":1,"title":"Workout","done":false},{"id":2,"title":"Read a book","done":true},{"id":3,"title":"Write code","done":false}]
```

## Swagger UI

The API also includes Swagger UI, which can be opened at:

`http://127.0.0.1:8000/docs`

It allows you to test all the endpoints directly from the browser.

## Notes

Data is stored in memory only. Restarting the server resets the tasks back to the three seed examples: Workout, Read a book, and Write code.

This is intentional for this stage of the assignment because a database has not been added yet.

## Me vs AI: A Comparison

As part of this assignment, I gave an AI, Claude, the exact same specification I built against without showing it my code. I then compared the two `main.py` files using `git diff --no-index`.

### What the AI did better and why

**Whitespace only titles on create**

My original check was:

```python
if not new_task.title or new_task.title is None:
```

The problem is that `not "   "` evaluates to `False` in Python. A string containing only spaces is still considered a non empty string.

Because of this, sending the following request:

```json
{"title": "   "}
```

would pass my validation and create a task with a blank title, even though my specification said this should return a 400 response.

The AI's version uses `.strip()` before checking whether the title is empty. This catches whitespace only titles correctly.

**ID counter instead of using `max()`**

I originally generated new IDs using:

```python
max(t["id"] for t in tasks) + 1
```

This works while there are tasks in the list, but it causes a `ValueError: max() arg is an empty sequence` once every task has been deleted.

The AI used a separate `next_id` counter instead. The counter continues increasing regardless of how many tasks currently exist, so creating a new task still works even when the task list is empty.

**Lookup structure**

I stored tasks in a list and searched through them whenever I needed to get, update, or delete a task.

For example:

```python
for task in tasks:
    if task["id"] == task_id:
```

The AI used a dictionary with the task ID as the key. This allows direct lookups in O(1) time instead of O(n).

For a small to do list this difference is not important, but using a dictionary is a better approach when the number of tasks grows.

I understand why each of these changes works. They are straightforward fixes once the issues are pointed out, and I could reproduce them myself. The `.strip()` issue in particular was a useful reminder that truthiness checks on strings do not handle whitespace only values.

## What the AI got wrong or changed quietly

The AI started with an empty task list, while my version included three example tasks: Workout, Read a book, and Write code.

My original prompt did not specify whether the list should start empty or contain sample data. This means it was not really a mistake against the specification. It was simply a design decision made differently by both of us.

However, this does affect the result of `GET /tasks` when the server starts, so it could matter if a grader expects one specific behavior.

The AI also did not ignore or change any of the status codes from my specification. The 200, 201, 204, 400, and 404 responses matched what I requested when I tested them.

## What my prompt did not specify

There were a few implementation details that I had not included in my original prompt, so the AI made its own decisions about them.

**Project structure**

The AI separated the project into `models.py` for the Pydantic schemas and `main.py` for the routes. I had not specified whether everything should be in one file or split across multiple files.

**Data structure**

The AI used a dictionary keyed by task ID, while I used a list. I had not specified which structure to use, which is why this also resulted in the difference between O(1) and O(n) lookups.

**Initial data**

I used three sample tasks while the AI started with an empty list. Again, the original prompt did not specify this behavior.

**Additional files**

The AI added a `requirements.txt` file and its own README. I had not specifically requested either of them, but both are reasonable additions for a project that needs to be installed and run by someone else.

## Bugs in my original version

This exercise helped me identify two actual bugs in my implementation:

1. Whitespace only titles could pass validation when creating a task. These should return a 400 response.

2. Creating a task after deleting all existing tasks caused an unhandled 500 error because `max()` was being called on an empty list.

I fixed these issues in the current version of `main.py`.
