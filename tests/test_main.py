from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


# Test 1: Health check
def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Test 2: Get all employees
def test_get_employees():
    response = client.get("/employees")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test 3: Find existing employee
def test_find_employee():
    response = client.get("/employees/Priya")

    assert response.status_code == 200
    assert response.json()["name"] == "Priya"


# Test 4: Employee not found
def test_employee_not_found():
    response = client.get("/employees/Unknown")

    assert response.status_code == 404


# Test 5: Invalid salary
def test_invalid_salary():
    response = client.post(
        "/employees", json={"name": "Test User", "department": "IT", "salary": -5}
    )

    assert response.status_code == 422


# Test 6: Empty employee name
def test_empty_name():
    response = client.post(
        "/employees", json={"name": "", "department": "IT", "salary": 30000}
    )

    assert response.status_code == 422


# Test 7: Successfully add a new employee
def test_add_employee(monkeypatch, tmp_path):
    test_file = tmp_path / "employees.json"
    test_file.write_text("[]")

    monkeypatch.setattr("src.main.DATA_FILE", test_file)

    response = client.post(
        "/employees", json={"name": "Test User", "department": "IT", "salary": 40000}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Employee added successfully"


# Test 8: Handle missing employee JSON file
def test_missing_employee_file(monkeypatch, tmp_path):
    missing_file = tmp_path / "missing.json"

    monkeypatch.setattr("src.main.DATA_FILE", missing_file)

    response = client.get("/employees")

    assert response.status_code == 200
    assert response.json() == []
