# Coding Standards for Corporate Training Project

## Technology Stack
- Always write backend code using **Python 3.11+** and **FastAPI**.
- Use **Pytest** for all unit testing suites.

## Code Style & Naming Conventions
- Variables and function names must use `snake_case`.
- Classes must use `PascalCase`.
- All asynchronous functions must explicitly include structured error handling (`try/except` blocks).

## Architecture Constraints
- Never mix business logic directly inside API routing files. Always abstract data handling to a dedicated `services/` layer.
- Do not use print statements (`print()`). Always utilize the Python native `logging` library.