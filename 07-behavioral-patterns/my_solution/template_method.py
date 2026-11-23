"""
Template Method pattern - refactor of the ETL pipelines.

Before: CSVPipeline, APIPipeline and DatabasePipeline each had their own run()
with the same 6 steps copied three times (connect, extract, transform,
validate, load, cleanup). Adding logging or changing the order meant editing
three classes.

After:
- DataPipeline (abstract) owns run(), the TEMPLATE METHOD: it fixes the order
  of the steps once, so no pipeline can skip or reorder one
- the common steps (connect, validate, load, cleanup) are written once
- each subclass only writes what is unique: extract() and transform()
- hooks (before_load, after_run) do nothing by default; a subclass may
  override them to add behaviour without touching the workflow
"""

import time
from abc import ABC, abstractmethod


class DataPipeline(ABC):
    source_type = "source"     # shown in the messages, e.g. "CSV file"
    name = "Generic"           # used in the final message
    required_fields = ()       # fields every record must have

    def __init__(self, source: str):
        self.source = source
        self.data = None

    # ------------------------------------------------------------------
    # The template method: the workflow is defined here and only here
    # ------------------------------------------------------------------
    def run(self) -> str:
        self.connect()
        self.data = self.extract()
        print(f"Extracted {len(self.data)} records")
        self.data = self.transform(self.data)
        self.validate(self.data)
        self.before_load(self.data)          # hook
        self.load(self.data)
        self.cleanup()
        self.after_run()                     # hook
        return f"{self.name} Pipeline finished"

    # --- steps that change for each pipeline (must be implemented) -----
    @abstractmethod
    def extract(self) -> list:
        """Read the raw records from the source."""

    @abstractmethod
    def transform(self, data: list) -> list:
        """Clean or enrich the records."""

    # --- common steps, written once ---------------------------------------
    def connect(self) -> None:
        print(f"Connecting to {self.source_type}: {self.source}")
        time.sleep(0.5)
        print(f"{self.name} connection established")

    def validate(self, data: list) -> None:
        print("Validating data...")
        for record in data:
            for field in self.required_fields:
                if field not in record:
                    raise ValueError(f"Invalid record structure: missing '{field}'")
        print("Validation passed")

    def load(self, data: list) -> None:
        print("Loading data to destination...")
        time.sleep(0.5)
        print(f"Loaded {len(data)} records successfully")

    def cleanup(self) -> None:
        print("Cleaning up resources...")
        self.data = None
        print("Cleanup complete")

    # --- hooks: optional, empty by default --------------------------------
    def before_load(self, data: list) -> None:
        pass

    def after_run(self) -> None:
        pass


class CSVPipeline(DataPipeline):
    source_type = "CSV file"
    name = "CSV"
    required_fields = ("id", "name")

    def extract(self) -> list:
        print("Extracting data from CSV...")
        return [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
        ]

    def transform(self, data: list) -> list:
        print("Transforming CSV data...")
        for record in data:
            record["age"] = int(record["age"])
            record["name"] = record["name"].upper()
        return data


class APIPipeline(DataPipeline):
    source_type = "API"
    name = "API"
    required_fields = ("user_id", "username")

    def extract(self) -> list:
        print("Extracting data from API...")
        return [
            {"user_id": 101, "username": "charlie", "score": 85},
            {"user_id": 102, "username": "diana", "score": 92},
        ]

    def transform(self, data: list) -> list:
        print("Transforming API data...")
        for record in data:
            record["score"] = int(record["score"])
            record["username"] = record["username"].lower()
            record["grade"] = "A" if record["score"] >= 90 else "B"
        return data


class DatabasePipeline(DataPipeline):
    source_type = "database"
    name = "Database"
    required_fields = ("product_id", "price")

    def extract(self) -> list:
        print("Extracting data from database...")
        return [
            {"product_id": 501, "product_name": "Laptop", "price": 1200},
            {"product_id": 502, "product_name": "Mouse", "price": 25},
        ]

    def transform(self, data: list) -> list:
        print("Transforming database data...")
        for record in data:
            record["price"] = float(record["price"])
            record["product_name"] = record["product_name"].title()
            record["tax"] = record["price"] * 0.2
        return data

    def before_load(self, data: list) -> None:
        # hook example: only the database pipeline reports its total
        total = sum(record["price"] + record["tax"] for record in data)
        print(f"Total value with tax: {total:.2f}")


# New pipeline added without touching DataPipeline or the other classes
class XMLPipeline(DataPipeline):
    source_type = "XML file"
    name = "XML"
    required_fields = ("order_id", "amount")

    def extract(self) -> list:
        print("Extracting data from XML...")
        return [
            {"order_id": "A-1", "customer": " emma ", "amount": "49.90"},
            {"order_id": "A-2", "customer": "louis", "amount": "120"},
        ]

    def transform(self, data: list) -> list:
        print("Transforming XML data...")
        for record in data:
            record["amount"] = float(record["amount"])  # XML values are text
            record["customer"] = record["customer"].strip().title()
        return data


if __name__ == "__main__":
    for pipeline in [
        CSVPipeline("data/users.csv"),
        APIPipeline("https://api.example.com/users"),
        DatabasePipeline("postgresql://localhost/mydb"),
        XMLPipeline("data/orders.xml"),
    ]:
        print(f"RUNNING {pipeline.name.upper()} PIPELINE")
        print("=" * 70)
        print(f"\n{pipeline.run()}\n")
