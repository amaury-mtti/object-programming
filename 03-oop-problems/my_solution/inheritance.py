"""
OOP Problems - Inheritance.

A subclass reuses everything from its parent class and only redefines
(overrides) what changes. super() calls the parent's version of a method.
"""


# ---------------------------------------------------------------------------
# Problem 1 - Vehicle, Car, Bicycle: method overriding
# ---------------------------------------------------------------------------
class Vehicle:
    def drive(self):
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self):
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self):
        return "Riding a bicycle"


# ---------------------------------------------------------------------------
# Problem 2 - Person, Student, Employee
# ---------------------------------------------------------------------------
class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self):
        return f"Hi, I'm {self.name}, I'm {self.age} and I live in {self.address}."


class Student(Person):
    def __init__(self, name, age, address, field_of_study):
        super().__init__(name, age, address)  # the parent sets name, age, address
        self.field_of_study = field_of_study

    def introduce(self):
        # reuse the parent's sentence and add the student part
        return super().introduce() + f" I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name, age, address, company):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self):
        return super().introduce() + f" I work at {self.company}."


# ---------------------------------------------------------------------------
# Problem 3 - BankAccount and SavingsAccount
# ---------------------------------------------------------------------------
class BankAccount:
    def __init__(self, account_number, balance=0.0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Return True if the withdrawal worked, False if the balance is too low."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, destination, amount):
        """Move money to another account. False if insufficient balance."""
        if not self.withdraw(amount):
            return False
        destination.deposit(amount)
        return True


class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0.0, interest_rate=0.02):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate  # 0.02 means 2 %

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest

    def check_balance(self):
        return self.balance


if __name__ == "__main__":
    for vehicle in [Vehicle(), Car(), Bicycle()]:
        print(vehicle.drive())  # polymorphism: same call, different result

    print(Student("Amaury", 19, "Paris", "AI & Data Science").introduce())
    print(Employee("Sophie", 30, "Monaco", "a family office").introduce())

    current = BankAccount("FR-001", 500)
    savings = SavingsAccount("FR-002", 1000, interest_rate=0.03)
    print("Transfer 200:", current.transfer(savings, 200))
    print("Transfer 1000:", current.transfer(savings, 1000))
    print("Interest added:", savings.add_interest())
    print("Savings balance:", savings.check_balance())
