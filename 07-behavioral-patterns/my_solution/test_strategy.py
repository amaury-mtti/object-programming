"""Tests for the Strategy pattern exercise (report formats).

They describe what my code must do. Written BEFORE the code:
run them, watch them fail (red), write the code, watch them pass (green).
"""
import json

import pytest

from strategy import (CSVFormatStrategy, ExcelFormatStrategy, FormatStrategy,
                      HTMLFormatStrategy, JSONFormatStrategy, PDFFormatStrategy,
                      ReportGenerator)

DATA = [
    {"name": "Sales Q1", "value": 15000},
    {"name": "Sales Q2", "value": 18000},
]


def test_strategy_interface_is_abstract():
    with pytest.raises(TypeError):
        FormatStrategy()


def test_csv_format():
    assert CSVFormatStrategy().format(DATA) == "name,value\nSales Q1,15000\nSales Q2,18000\n"


def test_json_format_is_valid_json():
    assert json.loads(JSONFormatStrategy().format(DATA)) == DATA


def test_pdf_format():
    report = PDFFormatStrategy().format(DATA)
    assert report.startswith("PDF REPORT")
    assert "Sales Q1" in report and "15000" in report


def test_excel_format():
    report = ExcelFormatStrategy().format(DATA)
    assert "Name\tValue" in report
    assert "Sales Q2\t18000" in report


def test_each_strategy_knows_its_file_extension():
    assert PDFFormatStrategy().extension == ".pdf"
    assert ExcelFormatStrategy().extension == ".xlsx"
    assert CSVFormatStrategy().extension == ".csv"
    assert JSONFormatStrategy().extension == ".json"


def test_switch_strategy_at_runtime():
    generator = ReportGenerator(DATA)
    generator.set_strategy(CSVFormatStrategy())
    csv_report = generator.generate_report()
    generator.set_strategy(JSONFormatStrategy())
    json_report = generator.generate_report()
    assert csv_report != json_report
    assert json.loads(json_report) == DATA


def test_no_strategy_raises_an_error():
    with pytest.raises(ValueError):
        ReportGenerator(DATA).generate_report()


def test_save_report_uses_the_strategy_extension(tmp_path):
    # tmp_path is a pytest fixture: a temporary folder deleted after the test
    generator = ReportGenerator(DATA)
    generator.set_strategy(CSVFormatStrategy())
    generator.save_report(str(tmp_path / "sales_report"))
    saved = tmp_path / "sales_report.csv"
    assert saved.exists()
    assert saved.read_text() == CSVFormatStrategy().format(DATA)


def test_html_added_without_modifying_the_others():
    html = HTMLFormatStrategy()
    assert isinstance(html, FormatStrategy)
    report = html.format(DATA)
    assert "<table" in report and "Sales Q1" in report
    assert html.extension == ".html"
