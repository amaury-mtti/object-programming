"""
Adapter pattern - make the legacy XML report generator work with the
new JSON analytics dashboard.

Before: every report function called the legacy system AND did its own
"conversion" (in fact it cheated with json.dumps on the original data,
so the XML was never really used).

After:
- ReportGeneratorInterface = what the dashboard expects: generate(data) -> JSON
- LegacyReportAdapter wraps LegacyReportGenerator (which we cannot modify),
  really converts its XML output into JSON, and implements the interface.
The dashboard never knows it is talking to a legacy system.
"""

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Existing code we are NOT allowed to change (external library)
# ---------------------------------------------------------------------------
class LegacyReportGenerator:
    def generate_report(self, data: dict) -> str:
        """Returns XML format - old system"""
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml


class AnalyticsDashboard:
    def display(self, json_data: str):
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")


# ---------------------------------------------------------------------------
# The target interface and the adapter
# ---------------------------------------------------------------------------
class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        """Return the report as a JSON string."""


class LegacyReportAdapter(ReportGeneratorInterface):
    def __init__(self, legacy_generator: LegacyReportGenerator):
        self._legacy = legacy_generator  # composition: the adapter HAS a legacy generator

    def generate(self, data: dict) -> str:
        xml_report = self._legacy.generate_report(data)   # 1. use the old system
        return json.dumps(self._xml_to_dict(xml_report))  # 2. translate XML -> JSON

    @staticmethod
    def _xml_to_dict(xml_report: str) -> dict:
        root = ET.fromstring(xml_report)
        return {child.tag: LegacyReportAdapter._convert(child.text) for child in root}

    @staticmethod
    def _convert(text):
        # XML stores everything as text: "1234" must become the number 1234 again
        if text is None:
            return None
        for cast in (int, float):
            try:
                return cast(text)
            except ValueError:
                pass
        return text


# ---------------------------------------------------------------------------
# Business functions, now without any conversion logic
# ---------------------------------------------------------------------------
def show_sales_report(report_generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard):
    report_data = {"total_sales": 150000, "orders": 1234, "avg_order": 121.55}
    dashboard.display(report_generator.generate(report_data))


def show_inventory_report(report_generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard):
    report_data = {"total_items": 5000, "low_stock": 45, "out_of_stock": 12}
    dashboard.display(report_generator.generate(report_data))


if __name__ == "__main__":
    report_generator = LegacyReportAdapter(LegacyReportGenerator())
    dashboard = AnalyticsDashboard()
    show_sales_report(report_generator, dashboard)
    show_inventory_report(report_generator, dashboard)
