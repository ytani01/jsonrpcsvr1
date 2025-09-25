# Codebase Structure

-   **`/` (Project Root):** Contains configuration files (`pyproject.toml`, `.gitignore`), `README.md`, and virtual environment related files.
-   **`src/jsonrpcsvr1/`:** The main application source directory.
    -   **`__main__.py`:** The primary entry point for the application.
    -   **`json_api.py`:** Likely defines the JSON-RPC API endpoints and their implementations.
    -   **`funcs/`:** Contains modules defining specific functions that can be exposed via the JSON-RPC API (e.g., `calc.py`, `echo.py`).
    -   **`utils/`:** Contains utility functions, such as `debug_log_env.py`.
-   **`samples/`:** Contains client-side examples for interacting with the JSON-RPC server (e.g., `sample1-client.py`, `sample2-client.py`).
-   **`tests/`:** Currently empty, indicating no automated tests are set up yet.
-   **`.venv/`:** Python virtual environment.
-   **`.git/`:** Git version control system files.
-   **`.mypy_cache/`, `.ruff_cache/`, `__pycache__/`:** Cache directories for various tools and Python bytecode.