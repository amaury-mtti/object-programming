# Creational patterns — UML class diagrams

The statement asks to draw the class diagram before coding. These are the
diagrams I used for `factory.py`, `builder.py` and `singleton.py`.

## 1. Factory — payment system

```mermaid
classDiagram
    class PaymentProcessor {
        <<abstract>>
        +str method
        +str error_message
        +validate(details: dict)* bool
        +calculate_fee(amount: float)* float
        +process(amount: float, details: dict) dict
    }
    class CreditCardProcessor {
        +validate(details: dict) bool
        +calculate_fee(amount: float) float
    }
    class BankTransferProcessor {
        +validate(details: dict) bool
        +calculate_fee(amount: float) float
    }
    class PayPalProcessor {
        +validate(details: dict) bool
        +calculate_fee(amount: float) float
    }
    class PaymentFactory {
        -dict _processors
        +register(payment_type: str, processor_class: type) None
        +get_processor(payment_type: str) PaymentProcessor
    }

    PaymentProcessor <|-- CreditCardProcessor
    PaymentProcessor <|-- BankTransferProcessor
    PaymentProcessor <|-- PayPalProcessor
    PaymentFactory ..> PaymentProcessor : creates
```

**Why it is better:** to add Apple Pay, I write an `ApplePayProcessor` class
and call `factory.register("apple_pay", ApplePayProcessor)`. No existing class
is modified (Open/Closed principle), and each processor can be tested alone.

## 2. Builder — employee onboarding

```mermaid
classDiagram
    class Employee {
        <<dataclass>>
        +str first_name
        +str last_name
        +str email
        +str department
        +str position
        +float salary
        +str start_date
        +int manager_id
        +bool has_laptop
        +bool has_parking
        +bool has_vpn_access
        +bool has_admin_rights
        +str contract_type
    }
    class EmployeeBuilder {
        -dict _data
        +with_name(first_name, last_name) EmployeeBuilder
        +with_email(email) EmployeeBuilder
        +with_job(department, position, salary) EmployeeBuilder
        +with_start_date(start_date) EmployeeBuilder
        +with_manager(manager_id) EmployeeBuilder
        +with_contact(phone, address, emergency_contact) EmployeeBuilder
        +with_equipment(laptop, parking) EmployeeBuilder
        +with_access(vpn, admin) EmployeeBuilder
        +with_office(office_location) EmployeeBuilder
        +with_contract(contract_type) EmployeeBuilder
        +build() Employee
    }
    class DeveloperBuilder {
        +DeveloperBuilder(first_name, last_name, email)
    }
    class InternBuilder {
        +InternBuilder(first_name, last_name, email, department)
    }

    EmployeeBuilder <|-- DeveloperBuilder
    EmployeeBuilder <|-- InternBuilder
    EmployeeBuilder ..> Employee : builds
```

**Why it is better:** every `with_...` method returns `self`, so the creation
reads like a sentence, and there are no more unnamed `None, False, True`
arguments to put in the right order. The validation lives in one place
(`build()`), and the presets guarantee that a developer always gets admin
rights and an intern never does.

## 3. Singleton — configuration manager

```mermaid
classDiagram
    class ConfigManager {
        <<singleton>>
        -ConfigManager _instance$
        -dict _config
        +int load_count
        +get_instance()$ ConfigManager
        +get(key: str, default) any
        +set(key: str, value) None
        -_load(path) dict
    }
    class AppService {
        +start_application()
    }
    class DatabaseService {
        +connect_database()
    }
    class EmailService {
        +send_email(to, subject)
    }
    class PaymentService {
        +process_payment(amount)
    }

    AppService ..> ConfigManager : get_instance()
    DatabaseService ..> ConfigManager : get_instance()
    EmailService ..> ConfigManager : get_instance()
    PaymentService ..> ConfigManager : get_instance()
```

(Underlined/`$` members are static: they belong to the class, not to an object.)

**Problems solved:**
1. *File read on every call* → the file is read once, on the first `get_instance()`.
2. *No shared state* → every service receives the same object.
3. *Changes not synchronized* → `set()` changes the shared object, so every service sees it.
4. *Hard to mock in tests* → there is now a single point (`ConfigManager._instance`) to replace.
