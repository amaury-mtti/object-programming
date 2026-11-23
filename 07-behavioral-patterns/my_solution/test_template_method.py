"""Tests for the Template Method exercise (ETL pipelines)."""
import pytest

import template_method
from template_method import (APIPipeline, CSVPipeline, DatabasePipeline,
                             DataPipeline, XMLPipeline)


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    # The pipelines call time.sleep(0.5) to simulate slow connections.
    # In tests we replace it with a function that does nothing, so the
    # tests stay instant. This is called "monkeypatching".
    monkeypatch.setattr(template_method.time, "sleep", lambda seconds: None)


def test_base_class_is_abstract():
    with pytest.raises(TypeError):
        DataPipeline("anything")


@pytest.mark.parametrize("pipeline, expected", [
    (CSVPipeline("data/users.csv"), "CSV Pipeline finished"),
    (APIPipeline("https://api.example.com/users"), "API Pipeline finished"),
    (DatabasePipeline("postgresql://localhost/mydb"), "Database Pipeline finished"),
    (XMLPipeline("data/orders.xml"), "XML Pipeline finished"),
])
def test_every_pipeline_runs(pipeline, expected):
    assert pipeline.run() == expected


def test_run_calls_the_steps_in_order():
    calls = []

    class SpyPipeline(CSVPipeline):
        def connect(self):
            calls.append("connect")
        def extract(self):
            calls.append("extract")
            return super().extract()
        def transform(self, data):
            calls.append("transform")
            return super().transform(data)
        def validate(self, data):
            calls.append("validate")
            super().validate(data)
        def load(self, data):
            calls.append("load")
        def cleanup(self):
            calls.append("cleanup")
            super().cleanup()

    SpyPipeline("x").run()
    assert calls == ["connect", "extract", "transform", "validate", "load", "cleanup"]


def test_csv_transform():
    pipeline = CSVPipeline("x")
    data = pipeline.transform(pipeline.extract())
    assert data[0]["name"] == "ALICE"


def test_validate_rejects_a_record_with_a_missing_field():
    with pytest.raises(ValueError):
        CSVPipeline("x").validate([{"id": 1}])  # "name" is missing


def test_cleanup_empties_the_data():
    pipeline = CSVPipeline("x")
    pipeline.run()
    assert pipeline.data is None


def test_api_grades():
    pipeline = APIPipeline("x")
    data = pipeline.transform(pipeline.extract())
    grades = {record["username"]: record["grade"] for record in data}
    assert grades == {"charlie": "B", "diana": "A"}  # 85 -> B, 92 -> A


def test_database_tax_is_20_percent():
    pipeline = DatabasePipeline("x")
    data = pipeline.transform(pipeline.extract())
    assert data[0]["tax"] == pytest.approx(240.0)  # 20 % of 1200


def test_hook_is_called_before_load():
    calls = []

    class HookedPipeline(CSVPipeline):
        def before_load(self, data):
            calls.append(len(data))

    HookedPipeline("x").run()
    assert calls == [2]


def test_xml_pipeline_converts_amounts():
    pipeline = XMLPipeline("x")
    data = pipeline.transform(pipeline.extract())
    assert data[0]["amount"] == 49.90 and data[0]["customer"] == "Emma"
