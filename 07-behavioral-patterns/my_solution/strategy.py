"""
Strategy pattern - refactor of the report generator.

Before: generate_report() and save_report() each had an if/elif chain on
format_type. Adding XML or Markdown meant modifying both methods (breaks the
Open/Closed principle), and no format could be tested on its own.

After:
- FormatStrategy = the contract: format(data) -> str, plus the file extension
- one class per format (PDF, Excel, CSV, JSON, then HTML)
- ReportGenerator = the context: it holds a strategy and delegates to it,
  and the strategy can be changed at runtime with set_strategy()
"""

import json
from abc import ABC, abstractmethod


class FormatStrategy(ABC):
    """Interface every report format must follow."""

    extension = ""

    @abstractmethod
    def format(self, data: list) -> str:
        """Turn the data into the report text."""


class PDFFormatStrategy(FormatStrategy):
    extension = ".pdf"

    def format(self, data: list) -> str:
        report = "PDF REPORT\n"
        report += "=" * 50 + "\n"
        for item in data:
            report += f"| {item['name']:20} | {item['value']:10} |\n"
        report += "=" * 50 + "\n"
        report += "End of PDF Report"
        return report


class ExcelFormatStrategy(FormatStrategy):
    extension = ".xlsx"

    def format(self, data: list) -> str:
        report = "EXCEL REPORT\n"
        report += "-" * 50 + "\n"
        report += "Name\tValue\n"
        for item in data:
            report += f"{item['name']}\t{item['value']}\n"
        report += "-" * 50 + "\n"
        return report


class CSVFormatStrategy(FormatStrategy):
    extension = ".csv"

    def format(self, data: list) -> str:
        report = "name,value\n"
        for item in data:
            report += f"{item['name']},{item['value']}\n"
        return report


class JSONFormatStrategy(FormatStrategy):
    extension = ".json"

    def format(self, data: list) -> str:
        return json.dumps(data, indent=2)


# Added AFTER the four classes above, without modifying any of them:
# this is the extensibility test asked by the statement.
class HTMLFormatStrategy(FormatStrategy):
    extension = ".html"

    def format(self, data: list) -> str:
        rows = "".join(
            f"    <tr><td>{item['name']}</td><td>{item['value']}</td></tr>\n"
            for item in data
        )
        return (
            "<table>\n"
            "    <tr><th>Name</th><th>Value</th></tr>\n"
            f"{rows}"
            "</table>"
        )


class ReportGenerator:
    """The context: it does not know any format, it asks its strategy."""

    def __init__(self, data: list, strategy: FormatStrategy = None):
        self.data = data
        self.strategy = strategy

    def set_strategy(self, strategy: FormatStrategy) -> None:
        self.strategy = strategy  # change the format at runtime

    def generate_report(self) -> str:
        if self.strategy is None:
            raise ValueError("Choose a format first with set_strategy()")
        return self.strategy.format(self.data)

    def save_report(self, filename: str) -> str:
        path = filename + self.strategy.extension  # no if/elif anymore
        with open(path, "w") as f:
            f.write(self.generate_report())
        return path


if __name__ == "__main__":
    data = [
        {"name": "Sales Q1", "value": 15000},
        {"name": "Sales Q2", "value": 18000},
        {"name": "Sales Q3", "value": 22000},
        {"name": "Sales Q4", "value": 25000},
    ]
    generator = ReportGenerator(data)

    for title, strategy in [
        ("PDF", PDFFormatStrategy()),
        ("CSV", CSVFormatStrategy()),
        ("JSON", JSONFormatStrategy()),
        ("HTML (NEW!)", HTMLFormatStrategy()),
    ]:
        print(f"=== {title} FORMAT ===")
        generator.set_strategy(strategy)  # same generator, new format
        print(generator.generate_report())
        print("\n" + "=" * 60 + "\n")
