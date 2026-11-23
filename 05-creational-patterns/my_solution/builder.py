"""
Builder pattern - refactor of the HR employee onboarding system.

Before: create_employee() took 17 positional arguments, so a call looked
like  ..., None, "+336...", None, None, False, True, True, True, ...
and nobody could tell which True meant what.

After:
- Employee   = the product, a simple data container (dataclass)
- EmployeeBuilder = small chainable methods; each one returns self so the
  calls can be chained, and build() validates everything at the end
- DeveloperBuilder / InternBuilder = presets with sensible defaults
  (a senior developer always gets admin rights, an intern never does)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: Optional[str] = None
    manager_id: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: Optional[str] = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    def __init__(self):
        # every field starts empty or with its default value
        self._data = {
            "first_name": None, "last_name": None, "email": None,
            "department": None, "position": None, "salary": None,
        }

    # --- chainable "with_" methods: each one sets a few fields, returns self
    def with_name(self, first_name, last_name):
        self._data["first_name"] = first_name
        self._data["last_name"] = last_name
        return self

    def with_email(self, email):
        self._data["email"] = email
        return self

    def with_job(self, department, position, salary):
        self._data["department"] = department
        self._data["position"] = position
        self._data["salary"] = salary
        return self

    def with_start_date(self, start_date):
        self._data["start_date"] = start_date
        return self

    def with_manager(self, manager_id):
        self._data["manager_id"] = manager_id
        return self

    def with_contact(self, phone=None, address=None, emergency_contact=None):
        self._data["phone"] = phone
        self._data["address"] = address
        self._data["emergency_contact"] = emergency_contact
        return self

    def with_equipment(self, laptop=False, parking=False):
        self._data["has_laptop"] = laptop
        self._data["has_parking"] = parking
        return self

    def with_access(self, vpn=False, admin=False):
        self._data["has_vpn_access"] = vpn
        self._data["has_admin_rights"] = admin
        return self

    def with_office(self, office_location):
        self._data["office_location"] = office_location
        return self

    def with_contract(self, contract_type):
        self._data["contract_type"] = contract_type
        return self

    def build(self) -> Employee:
        # all the validation is in ONE place, just before creating the object
        if not self._data["first_name"] or not self._data["last_name"]:
            raise ValueError("Name is required")
        if not self._data["email"] or "@" not in self._data["email"]:
            raise ValueError("Valid email is required")
        if not self._data["department"] or not self._data["position"]:
            raise ValueError("Department and position are required")
        if self._data["salary"] is None or self._data["salary"] < 0:
            raise ValueError("Salary cannot be negative")
        return Employee(**self._data)


class DeveloperBuilder(EmployeeBuilder):
    """Preset: a senior developer in Engineering with full access."""

    def __init__(self, first_name, last_name, email):
        super().__init__()
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job("Engineering", "Senior Developer", 75000)
             .with_equipment(laptop=True)
             .with_access(vpn=True, admin=True)
             .with_office("Paris HQ"))


class InternBuilder(EmployeeBuilder):
    """Preset: an intern with a laptop, no VPN and no admin rights."""

    def __init__(self, first_name, last_name, email, department):
        super().__init__()
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job(department, "Intern", 15000)
             .with_equipment(laptop=True)
             .with_contract("internship")
             .with_office("Paris HQ"))


if __name__ == "__main__":
    employee = (
        EmployeeBuilder()
        .with_name("John", "Doe")
        .with_email("john.doe@company.com")
        .with_job("Engineering", "Senior Developer", 75000)
        .with_equipment(laptop=True, parking=False)
        .with_access(vpn=True, admin=True)
        .build()
    )
    print(employee)

    dev = DeveloperBuilder("John", "Doe", "john.doe@company.com").build()
    print(dev)

    intern = (InternBuilder("Jane", "Smith", "jane.smith@company.com", "Marketing")
              .with_manager(42)
              .with_start_date("2024-02-01")
              .build())
    print(intern)
