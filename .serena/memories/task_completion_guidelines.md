# Task Completion Guidelines

When a task is completed, the following steps should be taken to ensure code quality and project stability:

1.  **Run Linters:** Execute `ruff check .` to ensure all linting rules are followed.
2.  **Run Formatters:** Execute `isort .` and `ruff format .` to ensure code formatting consistency.
3.  **Run Type Checkers:** Execute `mypy .` and `pyright .` to verify type correctness.
4.  **Manual Testing:** If automated tests are not yet implemented, perform manual testing of the changes, especially by interacting with the API via Swagger UI or `curl` commands.
5.  **Commit Changes:** Commit the changes with a clear and concise commit message.