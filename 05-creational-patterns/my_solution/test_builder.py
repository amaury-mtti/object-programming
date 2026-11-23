import pytest

from builder import DeveloperBuilder, Employee, EmployeeBuilder, InternBuilder


def test_fluent_builder():
    employee = (EmployeeBuilder()
                .with_name("John", "Doe")
                .with_email("john.doe@company.com")
                .with_job("Engineering", "Senior Developer", 75000)
                .with_equipment(laptop=True)
                .with_access(vpn=True, admin=True)
                .build())
    assert isinstance(employee, Employee)
    assert employee.has_laptop and employee.has_admin_rights
    assert not employee.has_parking
    assert employee.contract_type == "permanent"


def test_each_method_returns_the_builder():
    builder = EmployeeBuilder()
    assert builder.with_name("A", "B") is builder


def test_developer_preset():
    dev = DeveloperBuilder("John", "Doe", "john.doe@company.com").build()
    assert dev.department == "Engineering"
    assert dev.has_vpn_access and dev.has_admin_rights


def test_intern_preset():
    intern = InternBuilder("Jane", "Smith", "jane@company.com", "Marketing").with_manager(42).build()
    assert intern.contract_type == "internship"
    assert intern.manager_id == 42
    assert not intern.has_admin_rights


@pytest.mark.parametrize("builder", [
    EmployeeBuilder().with_email("a@b.com").with_job("IT", "Dev", 1),           # no name
    EmployeeBuilder().with_name("A", "B").with_email("bad").with_job("IT", "Dev", 1),
    EmployeeBuilder().with_name("A", "B").with_email("a@b.com").with_job("IT", "Dev", -5),
])
def test_validation_in_build(builder):
    with pytest.raises(ValueError):
        builder.build()
