# Exo 2 — ABCD Records 📼

Mermaid has no native use case diagram, so use cases are drawn as a
flowchart: round nodes are actors, stadium-shaped nodes are use cases, and the
box is the system boundary. Dotted arrows are `«include»` / `«extend»`.

---

## Level 1

### Task 1.1 — Simple use case diagram

```mermaid
flowchart LR
    member(("Member"))
    clerk(("Order Processing<br/>Clerk"))

    subgraph system ["ABCD Records — order system"]
        place([Place Order])
        verify([Verify Membership])
        process([Process Order])
        pay([Make Payment])
    end

    member --- place
    member --- pay
    clerk --- verify
    clerk --- process
```

### Task 1.2 — Basic class diagram

```mermaid
classDiagram
    class Member {
        -int member_id
        -str name
        -str address
        -str phone
        +place_order(items: list) Order
        +make_payment(order, amount: float)
    }
    class Order {
        -int order_id
        -date order_date
        -str status
        -float total
        +add_item(item, quantity: int)
        +calculate_total() float
    }
    class OrderProcessingClerk {
        -int clerk_id
        -str name
        +verify_membership(member_id: int) bool
        +process_order(order: Order)
    }

    Member "1" --> "0..*" Order : places
    OrderProcessingClerk "1" --> "0..*" Order : processes
    OrderProcessingClerk ..> Member : verifies
```

---

## Level 2

### Task 2.1 — Complete use case diagram

```mermaid
flowchart LR
    member(("Member"))
    royal(("Royal Member"))
    nonmember(("Non-Member"))
    clerk(("Order Processing<br/>Clerk"))
    collection(("Collection Dept.<br/>Clerk"))

    subgraph system ["ABCD Records — order system"]
        place([Place Order])
        verifyM([Verify Membership])
        verifyI([Verify Item Availability])
        unavailable([Order Unavailable Items])
        process([Process Order])
        discount([Apply Discount])
        invoice([Print Invoice])
        shipping([Print Shipping List])
        record([Save Order to Daily Records])
        pay([Make Payment])
        application([Send Membership Application])
    end

    royal -->|is a| member
    member --- place
    member --- pay
    royal --- unavailable
    nonmember --- place
    clerk --- verifyM
    clerk --- process
    collection --- pay

    place -.->|«include»| verifyM
    place -.->|«include»| verifyI
    process -.->|«include»| invoice
    process -.->|«include»| shipping
    process -.->|«include»| record
    application -.->|«extend»| verifyM
    unavailable -.->|«extend»| place
    discount -.->|«extend»| process
```

How to read it:
- **«include»** = always done: placing an order always verifies membership and
  availability; processing always prints the invoice and shipping list and
  saves the order to the daily records file (rule 8).
- **«extend»** = done only under a condition, and the arrow goes from the
  optional case to the base case: the application form is sent only if the
  membership check fails (rule 2), unavailable items and discounts only for
  Royal members (rules 3 and 4).
- **Royal Member → Member** is an actor generalization: a Royal member can do
  everything a member does, plus order unavailable items.

### Task 2.2 — Complete class diagram

```mermaid
classDiagram
    class Member {
        <<abstract>>
        #int member_id
        #str name
        #str address
        +place_order(lines: list) Order
        +get_discount_rate()* float
        +can_order_unavailable()* bool
    }
    class RoyalMember {
        -float discount_rate
        +get_discount_rate() float
        +can_order_unavailable() bool
    }
    class RegularMember {
        +get_discount_rate() float
        +can_order_unavailable() bool
    }
    class MembershipApplication {
        -int application_id
        -str applicant_name
        -str applicant_address
        -date sent_on
    }
    class Order {
        -int order_id
        -date order_date
        -str status
        +add_line(item, quantity: int)
        +subtotal() float
        +total() float
    }
    class OrderLine {
        -int quantity
        -bool backordered
        +line_total() float
    }
    class Item {
        <<abstract>>
        #str reference
        #str title
        #str artist
        #float price
        #int stock
        +is_available() bool
    }
    class CD {
        -int track_count
    }
    class Tape {
        -int length_minutes
    }
    class Invoice {
        -int invoice_number
        -float amount_due
        +print()
    }
    class ShippingList {
        -int list_number
        -str shipping_address
        +print()
    }
    class Payment {
        <<abstract>>
        #int payment_id
        #float amount
        #date paid_on
        +process()* bool
    }
    class Cash
    class Check {
        -str check_number
        -str bank
    }
    class BankDraft {
        -str draft_number
        -str issuing_bank
    }
    class Clerk {
        <<abstract>>
        #int clerk_id
        #str name
    }
    class OrderProcessingClerk {
        +verify_membership(member_id: int) bool
        +process_order(order: Order)
        +send_application(name: str, address: str) MembershipApplication
    }
    class CollectionDepartmentClerk {
        +record_payment(payment: Payment)
    }
    class DailyRecordsFile {
        -date day
        +save(order: Order)
    }

    Member <|-- RoyalMember
    Member <|-- RegularMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft
    Clerk <|-- OrderProcessingClerk
    Clerk <|-- CollectionDepartmentClerk

    Member "1" --> "0..*" Order : places
    Order "1" *-- "1..*" OrderLine : contains
    OrderLine "0..*" --> "1" Item : refers to
    Order "1" -- "1" Invoice : billed by
    Order "1" -- "0..1" ShippingList : shipped with
    Order "1" -- "0..*" Payment : paid by
    OrderProcessingClerk "1" --> "0..*" Order : processes
    OrderProcessingClerk "1" --> "0..*" MembershipApplication : sends
    CollectionDepartmentClerk "1" --> "0..*" Payment : records
    DailyRecordsFile "1" o-- "0..*" Order : records
```

Design choices:
- `OrderLine` sits between `Order` and `Item` so one order can hold several
  items with a quantity each (composition: lines do not exist without their order).
- The difference between Royal and Regular members is behaviour
  (`get_discount_rate()`, `can_order_unavailable()`), so it is modelled with
  **polymorphism**, not with `if member_type == "royal"`.
- `ShippingList` is `0..1` because an order whose items are all unavailable
  has nothing to ship yet.

### Scenario — a Royal member orders 2 CDs (one unavailable) and pays by check

Object diagram (snapshot of the objects at the end of the scenario; the prices
and the 10 % Royal discount are example values).

```mermaid
flowchart TB
    m["<b>alice : RoyalMember</b><br/>member_id = R-042<br/>discount_rate = 0.10"]
    o["<b>order_1001 : Order</b><br/>status = PARTIALLY_SHIPPED"]
    l1["<b>line1 : OrderLine</b><br/>quantity = 1<br/>backordered = False"]
    l2["<b>line2 : OrderLine</b><br/>quantity = 1<br/>backordered = True"]
    cd1["<b>cd_A : CD</b><br/>title = Kind of Blue<br/>price = 12.00<br/>stock = 8"]
    cd2["<b>cd_B : CD</b><br/>title = Blue Train<br/>price = 15.00<br/>stock = 0"]
    inv["<b>inv_77 : Invoice</b><br/>amount_due = 24.30<br/>(27.00 - 10 %)"]
    sl["<b>ship_55 : ShippingList</b><br/>items = cd_A"]
    chk["<b>pay_9 : Check</b><br/>check_number = 004512<br/>amount = 24.30"]

    m -->|places| o
    o -->|contains| l1
    o -->|contains| l2
    l1 -->|refers to| cd1
    l2 -->|refers to| cd2
    o -->|billed by| inv
    o -->|shipped with| sl
    o -->|paid by| chk
```

Because Alice is a Royal member, `cd_B` is accepted even though `stock = 0`:
its line is marked `backordered = True`, and only `cd_A` is on the shipping list
for now. A Regular member's order line for `cd_B` would have been refused.

---

## Level 3 — Advanced sequence diagrams

### 1. Complete order processing flow

```mermaid
sequenceDiagram
    actor M as Member
    actor OPC as Order Processing Clerk
    participant O as Order
    participant I as Item
    participant F as DailyRecordsFile
    actor CDC as Collection Dept. Clerk

    M->>OPC: place_order(member_id, items)
    OPC->>OPC: verify_membership(member_id)
    OPC->>O: create(member)
    loop for each requested item
        OPC->>I: is_available()
        I-->>OPC: True / False
        alt available, or member is Royal
            OPC->>O: add_line(item, quantity)
        else unavailable and Regular member
            OPC-->>M: item refused (out of stock)
        end
    end
    OPC->>O: total()
    O-->>OPC: amount after discount
    OPC->>OPC: print Invoice and ShippingList
    OPC->>F: save(order)
    OPC-->>M: invoice + shipment
    M->>CDC: make_payment(order, payment)
    CDC->>CDC: record_payment(payment)
    CDC-->>M: payment receipt
```

### 2. Membership verification (success and failure)

```mermaid
sequenceDiagram
    actor C as Customer
    actor OPC as Order Processing Clerk
    participant DB as MemberRegistry

    C->>OPC: place_order(member_id, items)
    OPC->>DB: find_member(member_id)
    alt member found
        DB-->>OPC: Member (Royal or Regular)
        OPC-->>C: order accepted, processing continues
    else not found
        DB-->>OPC: None
        OPC->>OPC: send_application(name, address)
        OPC-->>C: order refused + MembershipApplication form
        Note over C,OPC: The customer can order again once the application is accepted
    end
```

### 3. Payment processing (all types)

```mermaid
sequenceDiagram
    actor M as Member
    actor CDC as Collection Dept. Clerk
    participant P as Payment
    participant O as Order

    M->>CDC: make_payment(order_id, method, amount)
    CDC->>O: amount_due()
    O-->>CDC: amount
    alt Cash
        CDC->>P: create Cash(amount)
        P-->>CDC: accepted immediately
    else Check
        CDC->>P: create Check(amount, check_number, bank)
        P->>P: process() — wait until the bank clears the check
        P-->>CDC: cleared / bounced
    else Bank Draft
        CDC->>P: create BankDraft(amount, draft_number, bank)
        P->>P: process() — confirm with the issuing bank
        P-->>CDC: confirmed
    end
    alt payment OK
        CDC->>O: mark_paid(payment)
        CDC-->>M: receipt
    else payment failed
        CDC-->>M: payment rejected, please pay again
    end
```

### 4. Item reordering for Royal members

```mermaid
sequenceDiagram
    actor R as Royal Member
    actor OPC as Order Processing Clerk
    participant I as Item
    participant O as Order
    participant S as Supplier

    R->>OPC: place_order(member_id, [unavailable CD])
    OPC->>I: is_available()
    I-->>OPC: False
    OPC->>OPC: member.can_order_unavailable()
    alt Royal member
        OPC->>O: add_line(item, quantity, backordered = True)
        OPC->>S: reorder(item, quantity)
        S-->>OPC: expected delivery date
        OPC-->>R: order confirmed, item on backorder
        S->>OPC: deliver(item)
        OPC->>I: update stock
        OPC->>O: mark line shipped
        OPC-->>R: shipping list for the backordered item
    else Regular member
        OPC-->>R: item refused (only Royal members can order unavailable items)
    end
```
