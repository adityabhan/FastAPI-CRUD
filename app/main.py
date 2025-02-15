import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from models import (
    Todo,
    Session,
    get_session,
    create_db_and_tables,
    Department,
    select,
    Person,
)
from typing import Annotated
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # execute before starting app.
    create_db_and_tables()
    yield
    # execute before shutting down.
    print("GOOD BYE!")


app = FastAPI(lifespan=lifespan)


SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/", response_model=str)
def welcome():
    return "Welcome to Todos"


@app.post("/todo", response_model=Todo)
def add_todo(todo: Todo, session: Session = Depends(get_session)) -> Todo:
    """
    Add todos.
    """
    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@app.put("/todo/{todo_id}", response_model=Todo)
def update_todo_by_id(
    todo_id: int, todo_data: Todo, session: Session = Depends(get_session)
) -> Todo:
    """
    Edit existing todo with todo id.
    """
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(detail=f"No todo found with id= {todo_id}", status_code=404)

    update_data = todo_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@app.get("/todo/{todo_id}", response_model=Todo, description="Get a Todo with ID.")
def get_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo not found with id={todo_id}")
    return todo


# Department
@app.post("/department", response_model=Department)
def add_department(
    department: Department, session: Session = Depends(get_session)
) -> Department:
    """
    Add a Department.
    """
    session.add(department)
    try:
        session.commit()
    except LookupError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Invalid Department supplied.")
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Department already exists.")
    
    session.refresh(department)

    return department


@app.put("/department/{department_id}", response_model=Department)
def update_department_by_id(
    department_id: int,
    updated_data: Department,
    session: Session = Depends(get_session),
) -> Department:
    """
    Edit existing department with todo id.
    """
    department = session.get(Department, department_id)
    if not department:
        raise HTTPException(
            detail=f"No Department found with id= {department_id}", status_code=404
        )

    update_data = updated_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(department, key, value)

    session.add(department)
    session.commit()
    session.refresh(department)

    return department


@app.get("/department/{department_id}", response_model=Department)
def get_department(department_id: int, session: Session = Depends(get_session)):
    """
    Get a Department using department id.
    """
    department = session.get(Department, department_id)
    if not department:
        raise HTTPException(
            status_code=404, detail=f"Department not found with id={department_id}"
        )
    return department


@app.get("/departments", response_model=list[Department])
def get_departments(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> list[Department]:
    departments = session.exec(select(Department).offset(skip).limit(limit)).all()
    if not departments:
        raise HTTPException(status_code=404, detail="No Department exists.")
    return departments


# Person
@app.post("/person", response_model=Person)
def add_person(person: Person, session: Session = Depends(get_session)) -> Person:
    """
    Add a Person.
    """
    if person.department_id:
        department = session.get(Department, person.department_id)
        if not department:
            raise HTTPException(
                status_code=400,
                detail=f"No Such department with department_id={person.department_id} exists."
            )

    session.add(person)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400, detail=f"Email id {person.email} is already taken."
        )

    session.refresh(person)

    return person


@app.put("/person/{person_id}", response_model=Person)
def update_person_by_id(
    person_id: int,
    updated_data: Person,
    session: Session = Depends(get_session),
) -> Person:
    """
    Edit existing Person with person id.
    """
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(
            detail=f"No Person found with id= {person_id}", status_code=404
        )

    update_data = updated_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(person, key, value)

    session.add(person)
    session.commit()
    session.refresh(person)

    return person


@app.get("/person/{person_id}", response_model=Person)
def get_person_by_id(person_id: int, session: Session = Depends(get_session)):
    """
    Get a Person using person id.
    """
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(
            status_code=404, detail=f"Person not found with id={person_id}"
        )
    return person


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
