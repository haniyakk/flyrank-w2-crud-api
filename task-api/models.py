from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    """A task as stored and returned by the API."""
    id: int
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    """Body for POST /tasks. Only title is user-supplied; id and done are set by the server."""
    title: Optional[str] = None


class TaskUpdate(BaseModel):
    """Body for PUT /tasks/{id}. Both fields optional — only what's provided gets changed."""
    title: Optional[str] = None
    done: Optional[bool] = None
