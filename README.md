# Object Oriented Programming & Design Patterns in Python — Exercises

Exercises for the course **Object Oriented Programming & Design Patterns in Python**
(CentraleSupélec, AIDAMS bachelor, 2nd year).

**Author:** Amaury Martinotti

Each exercise has its own folder, with:
- `my_solution/` — my answers (scripts, Python code, tests, UML diagrams)
- `teacher_solution/` — the teacher's correction, used to compare with my work

## Exercises

| # | Folder | Topic | My solution |
|---|---|---|---|
| 1 | [`exo1_bash_scripting/`](exo1_bash_scripting/) | Shell & Bash scripting | Answers for parts 1–4 + `env_install.sh` |
| 2 | [`exo2_git_workflow/`](exo2_git_workflow/) | Git mini exercise | Commands and answers for parts 1–11, reflection questions, `install.sh` |
| 3 | [`exo3_oop_problems/`](exo3_oop_problems/) | Operator overloading & inheritance | `operator_overloading.py`, `inheritance.py` + tests |
| 4 | [`exo4_uml_modeling/`](exo4_uml_modeling/) | UML (Hospital, ABCD Records) | Class, use case, object and sequence diagrams in Mermaid |
| 5 | [`exo5_creational_patterns/`](exo5_creational_patterns/) | Factory, Builder, Singleton | Refactored code, UML diagrams + tests |
| 6 | [`exo6_structural_patterns/`](exo6_structural_patterns/) | Adapter, Decorator | Refactored code, UML diagrams + tests |

## Running the code and the tests

The repo is a [uv](https://docs.astral.sh/uv/) project: `pyproject.toml` lists
the dependencies and `uv.lock` pins their exact versions.

```bash
uv sync                                  # create .venv and install pytest (once)
uv run pytest -v                         # run all the tests
uv run pytest exo5_creational_patterns   # or the tests of one exercise
uv run python exo6_structural_patterns/my_solution/decorator.py   # run a demo
```

## About the teacher solutions

The teacher's solutions are locked on the course site, so the files in the
`teacher_solution/` folders stay on my computer and are excluded by
`.gitignore`. Only a README is published in each of those folders.
