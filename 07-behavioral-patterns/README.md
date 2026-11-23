# Exo 7 — Behavioral design patterns

Statement: <https://courses.dallard.tech/sys_design/behavioral_pattern/>

| File | Pattern | Refactored system |
|---|---|---|
| [`my_solution/strategy.py`](my_solution/strategy.py) | Strategy | Report generator (PDF, Excel, CSV, JSON, then HTML) |
| [`my_solution/template_method.py`](my_solution/template_method.py) | Template Method | ETL pipelines (CSV, API, database, then XML) |
| [`my_solution/diagrams.md`](my_solution/diagrams.md) | — | Problems found in the original code + UML class diagrams |
| `my_solution/test_*.py` | — | pytest tests (written before the code) |

```bash
uv run python 07-behavioral-patterns/my_solution/strategy.py
uv run python 07-behavioral-patterns/my_solution/template_method.py
uv run pytest 07-behavioral-patterns -v
```
