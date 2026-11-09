import csv
import json
import logging
from pathlib import Path
from typing import List, Optional, Union

import openpyxl
import pymupdf

# Logging setup
logging.basicConfig(level=logging.ERROR, format="%(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

# Project folder
BASE_DIR = Path(__file__).parent

# Employee CSV file
csv_file = BASE_DIR / "employees.csv"


# 1. Read employees from CSV
def read_employees(path: Path) -> List[dict]:
    employees = []

    with open(path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["salary"] = int(row["salary"])
            employees.append(row)

    return employees


# 2. Write employees into JSON
def write_json(employees: List[dict], path: Path) -> None:
    with open(path, "w") as file:
        json.dump(employees, file, indent=4)


# 3. Write high earners into CSV
def write_high_earners(employees: List[dict], path: Path) -> int:
    high_earners = []

    for employee in employees:
        if employee["salary"] > 50000:
            high_earners.append(employee)

    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "department", "salary"])

        writer.writeheader()
        writer.writerows(high_earners)

    return len(high_earners)


# 4. Create Excel file
def create_excel(employees: List[dict], path: Path) -> int:
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    sheet.append(["Name", "Department", "Salary"])

    for employee in employees:
        sheet.append([employee["name"], employee["department"], employee["salary"]])

    workbook.save(path)

    # Read Excel file back
    new_workbook = openpyxl.load_workbook(path)
    new_sheet = new_workbook.active

    return new_sheet.max_row - 1


# 5. Read first page of PDF
def read_pdf(path: Path) -> str:
    document = pymupdf.open(path)
    page = document[0]
    text = page.get_text()
    document.close()

    return text[:100]


# 6. Read file with error handling
def read_file(path: Path) -> Optional[dict]:
    try:
        with open(path, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        logger.error("File not found: %s", path.name)

    except json.JSONDecodeError:
        logger.error("Invalid JSON file: %s", path.name)

    return None


# 7. Find employee by name
def find_employee(name: str, employees: List[dict]) -> Optional[dict]:

    for employee in employees:
        if employee["name"].lower() == name.lower():
            return employee

    return None


# 8. Example function using Union type hint
def explain_value(value: Union[int, str]) -> str:
    return str(value)


# MAIN PROGRAM
if __name__ == "__main__":

    # Read CSV
    employees = read_employees(csv_file)

    # Create JSON
    write_json(employees, BASE_DIR / "employees.json")

    # Create high earners CSV
    count = write_high_earners(employees, BASE_DIR / "high_earners.csv")

    print(f"Rows read: {len(employees)} | " f"High earners written: {count}")

    # Create and read Excel
    excel_rows = create_excel(employees, BASE_DIR / "salary.xlsx")

    print(f"salary.xlsx created and read back: " f"{excel_rows} rows")

    # Find employee
    result = find_employee("Priya", employees)
    print("Found employee:", result)

    # Test missing file error
    read_file(BASE_DIR / "missing.txt")

    # Test PDF if one is available
    pdf_file = BASE_DIR / "sample.pdf"

    if pdf_file.exists():
        print("PDF text:", read_pdf(pdf_file))
    else:
        print("PDF test skipped: sample.pdf not found")

    print("Value example:", explain_value(100))
