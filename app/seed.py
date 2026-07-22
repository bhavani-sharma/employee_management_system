
from datetime import date
from common.data.database import SessionLocal
from infrastructure.schemas.employee_schema import Employee

db = SessionLocal()

try:
    employees = [
        Employee(
            emp_id = "I-005",
            name="Akash",
            email="akash@gmail.com",
            department="Engineering",
            role="Front End Developer",
            salary=50000,
            phone_number = "9663259630",
            is_eligible=False,  # must be True to be able to sign up
            pan_number="ABCMN1534F",
            emergency_contact_name="Aditya",
            emergency_contact_number="99122130451",
            blood_group="A+",
            address="Blr",
            joining_date=date(2026, 6, 13),
            date_of_birth=date(2005, 6, 29),
        ),
        Employee(
            emp_id = "I-006",
            name="Aditi Roy",
            email="aditi@gmail.com",
            department="Product",
            role="Manager",
            salary=65000,
            phone_number = "9877843410",
            is_eligible=True,
            pan_number="KJJEA7890I",
            emergency_contact_name="Jay",
            emergency_contact_number="9302630463",
            blood_group="O+",
            address="Blr",
            joining_date=date(2025, 7, 21),
            date_of_birth=date(1998, 1, 3),

        ),
    ]

    for employee in employees:
        existing = db.query(Employee).filter(Employee.email == employee.email).first()
        if existing:
            print(f"Skipping {employee.email} — already exists (id={existing.emp_id})")
            continue
        db.add(employee)
        db.commit()
        db.refresh(employee)
        print(f"Created employee id={employee.emp_id}: {employee.name} <{employee.email}> eligible={employee.is_eligible}")

finally:
    db.close()