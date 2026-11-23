# Exo 5 — Creational design patterns

Statement: <https://courses.dallard.tech/sys_design/creational_pattern/>

| File | Pattern | Refactored system |
|---|---|---|
| [`my_solution/factory.py`](my_solution/factory.py) | Factory | Payment system (credit card, bank transfer, PayPal) |
| [`my_solution/builder.py`](my_solution/builder.py) | Builder | HR employee onboarding |
| [`my_solution/singleton.py`](my_solution/singleton.py) + `config.json` | Singleton | Configuration manager |
| [`my_solution/diagrams.md`](my_solution/diagrams.md) | — | UML class diagram of each solution |
| `my_solution/test_*.py` | — | pytest tests |

```bash
python3 my_solution/factory.py     # or builder.py, singleton.py
pytest -v
```
