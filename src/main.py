import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Employee Data Service")

# Locate employees.json in the main week1test folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "employees.json"


# Employee input validation
class Employee(BaseModel):
    name: str = Field(min_length=1)
    department: str
    salary: float = Field(gt=0)


# Read employee data
def read_employees() -> List[dict]:
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


# Save employee data
def save_employees(employees: List[dict]) -> None:
    with open(DATA_FILE, "w") as file:
        json.dump(employees, file, indent=4)


# 1. Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}


# 2. Get all employees
@app.get("/employees")
def get_employees():
    return read_employees()


# 3. Find employee by name
@app.get("/employees/{name}")
def get_employee(name: str):
    employees = read_employees()

    for employee in employees:
        if employee["name"].lower() == name.lower():
            return employee

    raise HTTPException(status_code=404, detail="Employee not found")


# 4. Add a new employee
@app.post("/employees")
def add_employee(employee: Employee):
    employees = read_employees()

    new_employee = employee.model_dump()
    employees.append(new_employee)

    save_employees(employees)

    return {"message": "Employee added successfully", "employee": new_employee}
