# Object-Oriented Programming & Design Patterns in Python

Myexercises for the **Object-Oriented Programming & Design Patterns in Python**
course taught by **Benjamin Dallard**.

## About me

I'm **Amaury Martinotti**, a second-year student in the **AIDAMS** bachelor
(Artificial Intelligence, Data and Management Sciences), the joint program of
**ESSEC Business School** and **CentraleSupélec**.

This repository follows the course step by step: it starts with the command
line and Git, moves on to object-oriented programming in Python, then UML
modeling, and ends with design patterns.

## How the repo is organized

One numbered folder per exercise, in the order of the course. Inside each one:
- `my_solution/` contains my work: scripts, Python code with tests, UML diagrams
- `teacher_solution/` links to the official correction, which I used to compare
  my approach with the teacher's

| Folder | Topic | What I did |
|---|---|---|
| [`01-bash-scripting/`](01-bash-scripting/) | Shell & Bash scripting | Set up my terminal (zsh, Oh My Zsh, Git plugin) and wrote `env_install.sh`, a script that installs a Python environment depending on the OS |
| [`02-git-workflow/`](02-git-workflow/) | Git | The full workflow: commits, branches, merge, push, clone, plus the reflection questions |
| [`03-oop-problems/`](03-oop-problems/) | Operator overloading & inheritance | Complex numbers, vectors, matrices, bank accounts... with pytest tests |
| [`04-uml-modeling/`](04-uml-modeling/) | UML | Hospital Management System and ABCD Records: class, use case, object and sequence diagrams |
| [`05-creational-patterns/`](05-creational-patterns/) | Factory, Builder, Singleton | Refactoring of "spaghetti" code, with a UML diagram and tests for each pattern |
| [`06-structural-patterns/`](06-structural-patterns/) | Adapter, Decorator | Same approach: refactoring, UML diagram, tests |

## My setup

macOS with zsh and Oh My Zsh, Python 3.13, and [uv](https://docs.astral.sh/uv/)
to manage the environment (`pyproject.toml` lists the dependencies, `uv.lock`
pins their exact versions).

## Running the code

```bash
uv sync                                 # create .venv and install pytest (once)
uv run pytest -v                        # run all the tests
uv run pytest 05-creational-patterns    # or only one exercise
uv run python 06-structural-patterns/my_solution/decorator.py   # run a demo
```


