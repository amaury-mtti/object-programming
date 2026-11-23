# Exo 1 — Hospital Management System 🏥

Diagrams are written in [Mermaid](https://mermaid.js.org/), so GitHub draws
them directly in this page.

---

## Task 1 — Basic class diagram (Patient, Doctor, Organizer)

```mermaid
classDiagram
    class Patient {
        -int patient_id
        -str name
        -str email
        -str password
        +post_health_problem(description: str) HealthProblem
        +receive_prescription(prescription)
        +pay(amount: float, method: str)
    }
    class Doctor {
        -int doctor_id
        -str name
        -str speciality
        -str password
        +review_problem(problem)
        +write_prescription(problem) Prescription
        +receive_payment(amount: float)
    }
    class Organizer {
        -int organizer_id
        -str name
        -str password
        +read_problem(problem)
        +consult_doctor(doctor, problem)
        +send_prescription(patient, prescription)
        +forward_payment(doctor, amount: float)
        +create_member(name: str, role: str) int
    }

    Organizer "1" --> "0..*" Patient : manages
    Organizer "1..*" --> "0..*" Doctor : consults
```

**Reading the multiplicities:** one organizer manages any number of patients;
there is at least one organizer, and each organizer can consult several
doctors. Patients and doctors never talk directly: everything goes through the
organizer (steps 2 to 6 of the workflow).

---

## Task 2 — Complete class diagram (6 classes + payment types)

```mermaid
classDiagram
    class Patient {
        -int patient_id
        -str name
        -str email
        -str password
        +post_health_problem(description: str) HealthProblem
        +pay(prescription, payment: Payment)
    }
    class Doctor {
        -int doctor_id
        -str name
        -str speciality
        +write_prescription(problem) Prescription
        +receive_payment(payment: Payment)
    }
    class Organizer {
        -int organizer_id
        -str name
        +assign_doctor(problem, doctor)
        +send_prescription(patient, prescription)
        +forward_payment(payment, doctor)
        +create_member(name: str, role: str) int
    }
    class HealthProblem {
        -int problem_id
        -str description
        -date submitted_on
        +get_details() str
    }
    class Prescription {
        -int prescription_id
        -str content
        -date issued_on
        -float price
    }
    class Payment {
        <<abstract>>
        -int payment_id
        -float amount
        -date paid_on
        +process()* bool
    }
    class CheckPayment {
        -str check_number
        -str bank_name
        +process() bool
    }
    class CashPayment {
        -float amount_received
        +process() bool
    }
    class CreditCardPayment {
        -str card_number
        -str expiry_date
        +process() bool
    }

    Patient "1" *-- "0..*" HealthProblem : posts
    Organizer "1" --> "0..*" HealthProblem : reads
    Doctor "1" --> "0..*" Prescription : writes
    HealthProblem "1" -- "0..1" Prescription : answered by
    Patient "1" --> "0..*" Payment : makes
    Prescription "1" -- "0..1" Payment : paid by
    Organizer "1" --> "0..*" Payment : forwards
    Payment <|-- CheckPayment
    Payment <|-- CashPayment
    Payment <|-- CreditCardPayment
```

**Design choices:**
- **Composition** between `Patient` and `HealthProblem`: a health problem only
  exists for the patient who posted it (if the patient account is deleted, so
  are their problems).
- **Inheritance** for the payment types rather than an enumeration: each type
  needs its own data (check number, card number...) and its own way of being
  processed, so `process()` is abstract and redefined in each subclass.

### Sequence diagram — a patient submits a problem, receives a prescription and pays

```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant D as Doctor

    P->>O: post_health_problem(description)
    activate O
    O-->>P: problem_id
    O->>D: consult_doctor(problem)
    activate D
    D->>D: review_problem(problem)
    D-->>O: write_prescription(problem) : Prescription
    deactivate D
    O->>P: send_prescription(prescription)
    deactivate O

    P->>O: pay(prescription, CreditCardPayment)
    activate O
    O->>O: payment.process()
    O-->>P: payment receipt
    O->>D: forward_payment(payment)
    deactivate O
```

---

## Task 3 — Advanced model

### Final class diagram

```mermaid
classDiagram
    class User {
        <<abstract>>
        #int user_id
        #str name
        #str email
        #str password_hash
        +login(email: str, password: str) bool
        +logout()
    }
    class Patient {
        -date birth_date
        +submit_problem(description: str) HealthProblem
        +get_past_prescriptions() list
        +pay(prescription, method: PaymentMethod) Payment
    }
    class Doctor {
        -str speciality
        -str license_number
        +write_prescription(problem, content: str) Prescription
    }
    class Organizer {
        +create_member(name: str, role: str) User
        +reset_password(user: User)
        +assign_doctor(problem, doctor)
        +send_prescription(prescription)
        +forward_payment(payment)
        +update_system()
    }
    class HealthProblem {
        -int problem_id
        -str description
        -ProblemStatus status
        -datetime created_at
        -datetime updated_at
        +change_status(new_status: ProblemStatus)
    }
    class ProblemStatus {
        <<enumeration>>
        PENDING
        IN_REVIEW
        RESOLVED
    }
    class Prescription {
        -int prescription_id
        -str content
        -float price
        -datetime issued_at
        -Prescription previous
        +renew() Prescription
    }
    class Payment {
        -int payment_id
        -float amount
        -PaymentStatus status
        -datetime paid_at
        -datetime forwarded_at
        +execute() bool
    }
    class PaymentStatus {
        <<enumeration>>
        PENDING
        RECEIVED
        FORWARDED
    }
    class PaymentMethod {
        <<interface>>
        +pay(amount: float)* bool
    }
    class CheckPayment {
        -str check_number
        +pay(amount: float) bool
    }
    class CashPayment {
        +pay(amount: float) bool
    }
    class CreditCardPayment {
        -str card_number
        -str expiry_date
        +pay(amount: float) bool
    }

    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Patient "1" *-- "0..*" HealthProblem : submits
    HealthProblem --> ProblemStatus
    Organizer "1" --> "0..*" HealthProblem : assigns
    HealthProblem "0..*" --> "0..1" Doctor : assigned to
    HealthProblem "1" -- "0..*" Prescription : answered by
    Doctor "1" --> "0..*" Prescription : writes
    Prescription "0..1" --> "0..1" Prescription : renews
    Prescription "1" -- "0..1" Payment : paid by
    Payment --> PaymentStatus
    Payment o-- "1" PaymentMethod : uses
    PaymentMethod <|.. CheckPayment
    PaymentMethod <|.. CashPayment
    PaymentMethod <|.. CreditCardPayment
```

What changed compared with Task 2:
- **`User` superclass** holds what every actor shares (id, name, password,
  `login()` / `logout()`), so it is written only once.
- **Status tracking:** `HealthProblem.status` uses the `ProblemStatus`
  enumeration (`PENDING` → `IN_REVIEW` → `RESOLVED`); `Payment` has its own
  status (`PENDING` → `RECEIVED` → `FORWARDED`).
- **Timestamps** (`created_at`, `issued_at`, `paid_at`...) on every event.
- **Past prescriptions:** a prescription can point to the one it `renews`, and
  `Patient.get_past_prescriptions()` gives the history.
- **Payment with polymorphism:** `Payment` no longer has subclasses; it *has* a
  `PaymentMethod`. `Payment.execute()` just calls `method.pay(amount)`, and each
  concrete method does it its own way.

### SSD 1 — Patient registration (the organizer creates a new member)

```mermaid
sequenceDiagram
    actor O as Organizer
    participant S as System
    actor P as Patient

    O->>S: create_member(name, email, role = "patient")
    S->>S: check that the email is not used yet
    alt email already used
        S-->>O: error: member already exists
    else new email
        S->>S: generate user_id and temporary password
        S-->>O: user_id
        S->>P: send credentials (user_id, temporary password)
        P->>S: login(email, temporary password)
        S-->>P: ask to choose a new password
        P->>S: change_password(new password)
        S-->>P: account active
    end
```

### SSD 2 — Consultation flow (from problem submission to prescription delivery)

```mermaid
sequenceDiagram
    actor P as Patient
    actor O as Organizer
    actor D as Doctor
    participant S as System

    P->>S: submit_problem(description)
    S-->>P: problem_id (status = PENDING)
    O->>S: list_pending_problems()
    S-->>O: pending problems
    O->>S: assign_doctor(problem_id, doctor_id)
    S-->>O: status = IN_REVIEW
    S->>D: notify new problem to review
    D->>S: get_problem(problem_id)
    S-->>D: description + past prescriptions of the patient
    D->>S: write_prescription(problem_id, content, price)
    S-->>D: prescription_id
    O->>S: send_prescription(prescription_id)
    S-->>O: status = RESOLVED
    S->>P: prescription available
```

### SSD 3 — Payment processing (the patient pays, the organizer forwards it)

```mermaid
sequenceDiagram
    actor P as Patient
    actor O as Organizer
    actor D as Doctor
    participant S as System

    P->>S: pay(prescription_id, method)
    alt credit card
        S->>S: CreditCardPayment.pay(amount)
    else check
        S->>S: CheckPayment.pay(amount) (pending until the check clears)
    else cash
        S->>S: CashPayment.pay(amount) (recorded by the organizer)
    end
    alt payment accepted
        S-->>P: receipt (status = RECEIVED)
        O->>S: forward_payment(payment_id)
        S->>D: transfer amount
        S-->>O: status = FORWARDED
    else payment refused
        S-->>P: error: payment refused, try another method
    end
```

---

## Questions to consider

**1. How would you handle a patient consulting multiple doctors?**
The doctor is not linked to the patient directly but to each `HealthProblem`
(`HealthProblem "0..*" --> "0..1" Doctor`). A patient with three problems can
therefore have three different doctors. If one problem needs several opinions,
the multiplicity becomes `0..*` and each doctor writes their own
`Prescription` for the same problem.

**2. Should prescriptions be reusable? How would you model that?**
Not as-is: a prescription is a medical document tied to one patient, one
problem and one date, so modifying an old one would destroy the history. But a
treatment can be *renewed*: `renew()` creates a **new** `Prescription` that
points to the previous one (`previous` attribute / `renews` self-association).
This keeps the history intact and lets the doctor see past prescriptions.

**3. What design pattern fits the payment system?**
The **Strategy** pattern: `Payment` holds a `PaymentMethod` (the strategy) and
calls `method.pay(amount)` without knowing whether it is a check, cash or a
card. Adding a new method (bank transfer, Apple Pay...) means adding one class,
without modifying `Payment`. A **Factory** can be added on top to create the
right `PaymentMethod` from the patient's choice.

**4. How do you ensure data integrity when payments are processed?**
- Treat a payment as a **transaction**: either everything is saved (payment +
  status change) or nothing is (rollback on error).
- Use the **status** as a state machine: only `PENDING → RECEIVED → FORWARDED`
  is allowed, so a payment cannot be forwarded twice or before being received.
- Give each payment a unique id (idempotency) so a double click does not charge
  the patient twice.
- Check the amount against `Prescription.price`, keep timestamps for an audit
  trail, and never store full card numbers (use a payment provider token).
