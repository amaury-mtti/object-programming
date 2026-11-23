from inheritance import (Bicycle, BankAccount, Car, Employee, Person,
                         SavingsAccount, Student, Vehicle)


def test_drive_is_overridden():
    assert Vehicle().drive() == "Driving a vehicle"
    assert Car().drive() == "Driving a car"
    assert Bicycle().drive() == "Riding a bicycle"
    assert isinstance(Car(), Vehicle)


def test_introduce_is_personalized():
    base = Person("Ana", 20, "Paris").introduce()
    student = Student("Ana", 20, "Paris", "Economics").introduce()
    employee = Employee("Ana", 20, "Paris", "ESSEC").introduce()
    assert student.startswith(base) and "Economics" in student
    assert employee.startswith(base) and "ESSEC" in employee


def test_deposit_and_withdraw():
    account = BankAccount("A1", 100)
    account.deposit(50)
    assert account.withdraw(30) is True
    assert account.balance == 120
    assert account.withdraw(500) is False
    assert account.balance == 120


def test_transfer():
    source, destination = BankAccount("A1", 100), BankAccount("A2", 0)
    assert source.transfer(destination, 60) is True
    assert (source.balance, destination.balance) == (40, 60)
    assert source.transfer(destination, 100) is False
    assert (source.balance, destination.balance) == (40, 60)


def test_savings_account():
    savings = SavingsAccount("S1", 1000, interest_rate=0.05)
    assert savings.add_interest() == 50
    assert savings.check_balance() == 1050
    assert isinstance(savings, BankAccount)
