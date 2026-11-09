import csv


# 1. Function to calculate bonus
def calculate_bonus(salary, rate=0.1, *extras, **options):
    bonus = salary * rate + sum(extras)

    if "cap" in options:
        bonus = min(bonus, options["cap"])

    return bonus


# 2. Employee class
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"{self.name} - {self.salary}"

    @property
    def annual_salary(self):
        return self.salary * 12


# 3. Decorator to log function calls
def log_call(func):
    def wrapper(*args, **kwargs):
        print("Calling get_details")
        return func(*args, **kwargs)

    return wrapper


# 4. Manager class (Inheritance)
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self):
        return f"{self.name} - {self.salary} - Team Size: {self.team_size}"


# 5. Read employee data from CSV
with open("employees.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row["name"]
        salary = int(row["salary"])

        # Salary category
        if salary < 50000:
            category = "Low Salary"
        elif salary < 70000:
            category = "Medium Salary"
        else:
            category = "High Salary"

        print(f"{name} - {category}")


# 6. Calculate bonus example
bonus = calculate_bonus(50000, 0.1, 1000, 2000, cap=7000)
print("\nBonus:", bonus)


# 7. Create Manager object
manager = Manager("Divya", 75000, 5)

print(manager.get_details())

# 8. Annual salary example
print("Annual Salary:", manager.annual_salary)
