from enum import Enum


class Department(str, Enum):
    Engineering = "Engineering"
    HR = "HR"
    Sales = "Sales"
    Finance = "Finance"
    Marketing = "Marketing"
    Testing = "Testing"


class Roles(str, Enum):
    Intern = "Intern"
    Manager = "Manager"
    Admin = "Admin"
    Developer = "Developer"
    Lead = "Lead"


class Genders(str, Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"


class EmployeeSortField(str, Enum):
    id = "id"
    name = "name"
    email = "email"
    department = "department"
    salary = "salary"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class Currency(str, Enum):
    INR = "INR"
    USD = "USD"
    JPY = "JPY"
    SGD = "SGD"
    GBP = "GBP"
