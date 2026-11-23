import json

import pytest

from adapter import (AnalyticsDashboard, LegacyReportAdapter, LegacyReportGenerator,
                     ReportGeneratorInterface, show_sales_report)


def test_adapter_returns_valid_json_with_types():
    adapter = LegacyReportAdapter(LegacyReportGenerator())
    data = {"total_sales": 150000, "avg_order": 121.55, "region": "EU"}
    assert json.loads(adapter.generate(data)) == data


def test_adapter_implements_interface():
    assert isinstance(LegacyReportAdapter(LegacyReportGenerator()), ReportGeneratorInterface)


def test_adapter_really_uses_the_legacy_system():
    class SpyLegacy(LegacyReportGenerator):
        called = False

        def generate_report(self, data):
            SpyLegacy.called = True
            return super().generate_report(data)

    LegacyReportAdapter(SpyLegacy()).generate({"a": 1})
    assert SpyLegacy.called


def test_dashboard_displays_report(capsys):
    show_sales_report(LegacyReportAdapter(LegacyReportGenerator()), AnalyticsDashboard())
    output = capsys.readouterr().out
    assert "total_sales: 150000" in output and "avg_order: 121.55" in output


def test_interface_is_abstract():
    with pytest.raises(TypeError):
        ReportGeneratorInterface()
