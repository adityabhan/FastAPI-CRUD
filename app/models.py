from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from pydantic import EmailStr, field_validator
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum


class TodoMapping(SQLModel, table=True):
    todo_id: int = Field(foreign_key="todo.id", primary_key=True)
    people_id: int = Field(foreign_key="person.id", primary_key=True)

    # back-references
    todo: Optional["Todo"] = Relationship(back_populates="todo_mapping")
    person: Optional["Person"] = Relationship(back_populates="people_mapping")


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: str = Field(max_length=1024)
    completed: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    completed_on: Optional[datetime]

    # One Todo can be linked to many TodoMapping entries (many-to-many with Person)
    todo_mapping: List[TodoMapping] = Relationship(back_populates="todo")


class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, nullable=False, unique=True)

    # back populates  (one to many) one department can have many person
    person: list["Person"] = Relationship(back_populates="department")


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)

    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    department: Optional[Department] = Relationship(back_populates="person")

    # one person can be associated with many todos (Many to Many)
    people_mapping: List[TodoMapping] = Relationship(back_populates="person")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
