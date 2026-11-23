# Structural patterns — UML class diagrams

## 1. Adapter — legacy XML reports in a JSON dashboard

```mermaid
classDiagram
    class ReportGeneratorInterface {
        <<interface>>
        +generate(data: dict)* str
    }
    class LegacyReportAdapter {
        -LegacyReportGenerator _legacy
        +generate(data: dict) str
        -_xml_to_dict(xml_report: str)$ dict
        -_convert(text: str)$ any
    }
    class LegacyReportGenerator {
        +generate_report(data: dict) str
    }
    class AnalyticsDashboard {
        +display(json_data: str)
    }

    ReportGeneratorInterface <|.. LegacyReportAdapter : implements
    LegacyReportAdapter o-- LegacyReportGenerator : wraps
    AnalyticsDashboard ..> ReportGeneratorInterface : uses JSON from
```

**Problems solved:**
- *Incompatible interfaces* → the adapter exposes `generate()` returning JSON,
  which is what the dashboard expects.
- *Conversion logic repeated* → the XML → JSON translation is written once,
  inside the adapter.
- *Can't modify the legacy system* → we never touch `LegacyReportGenerator`,
  we only wrap it.
- *Tight coupling* → the report functions only know the interface, so the
  legacy system could be replaced by a native JSON generator without
  changing them.

## 2. Decorator — order pricing

```mermaid
classDiagram
    class OrderComponent {
        <<interface>>
        +get_cost()* float
        +get_description()* str
    }
    class BaseOrder {
        +float base_price
        +get_cost() float
        +get_description() str
    }
    class OrderDecorator {
        <<abstract>>
        -OrderComponent _order
        +base_price float
        +get_cost() float
        +get_description() str
    }
    class ExpressShippingDecorator {
        +COST = 15.00
    }
    class InsuranceDecorator {
        +RATE = 0.05
    }
    class GiftWrapDecorator {
        +COST = 5.00
    }
    class DiscountDecorator {
        +float percent
    }
    class PremiumMemberDecorator {
        +RATE = 0.10
    }

    OrderComponent <|.. BaseOrder
    OrderComponent <|.. OrderDecorator
    OrderDecorator o-- OrderComponent : wraps
    OrderDecorator <|-- ExpressShippingDecorator
    OrderDecorator <|-- InsuranceDecorator
    OrderDecorator <|-- GiftWrapDecorator
    OrderDecorator <|-- DiscountDecorator
    OrderDecorator <|-- PremiumMemberDecorator
```

The key point is the double link between `OrderDecorator` and
`OrderComponent`: a decorator **is** an order (inheritance) and **has** an
order (aggregation). That is why decorators can be stacked:
`PremiumMemberDecorator(DiscountDecorator(GiftWrapDecorator(...)))`.

**Problems solved:**
- *Boolean flag explosion* → each option is a class; adding one never adds a parameter.
- *Single method does everything* → each decorator has one responsibility.
- *Hard to extend* → a new option is a new decorator, no existing code changes.
- *Can't reuse options* → `InsuranceDecorator` can wrap any order.
- *Order of operations unclear* → the wrapping order **is** the calculation order
  (here the discounts apply after shipping, insurance and gift wrap, which gives
  95.625€ for a 100€ order, the same result as the original code).
