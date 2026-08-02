from datetime import date

from common.data.database import SessionLocal
from employee.infrastructure.entity.entity import Employee

db = SessionLocal()

try:
    employees = [
        Employee(
            name="Jake M",
            email="jake@gmail.com",
            department="Engineering",
            role="Admin",
            currency="INR",
            salary=50000,
            phone_number="8819729630",
            is_eligible=True,  # must be True to be able to sign up
            pan_number="ABASO1534F",
            emergency_contact_name="Shekar",
            emergency_contact_number="99620030451",
            blood_group="O+",
            address="123 Street, Pune",
            joining_date=date(2025, 6, 13),
            date_of_birth=date(2002, 10, 11),
            gender="Male",
            created_by_employee_id=0,
            last_modified_by_employee_id=0,
        ),
    ]

    for employee in employees:
        existing = db.query(Employee).filter(Employee.email == employee.email).first()
        if existing:
            print(
                f"Skipping {employee.email} — already exists (id={existing.employee_id})"
            )
            continue
        db.add(employee)
        db.commit()
        db.refresh(employee)
        print(employee.id)

        print(
            f"Created employee id={employee.id}: {employee.name} <{employee.email}> eligible={employee.is_eligible}"
        )

finally:
    db.close()
