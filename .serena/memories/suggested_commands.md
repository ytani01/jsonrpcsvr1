# Suggested Commands

## Project Setup

1.  **Clone repositories (if not already done):**
    ```bash
    git clone https://github.com/ytani01/pyclickutils.git
    git clone https://github.com/ytani01/jsonrpcsvr1.git
    ```

2.  **Navigate to project directory:**
    ```bash
    cd jsonrpcsvr1
    ```

## Running the Server

-   **Start the JSON-RPC server:**
    ```bash
    uv run jsonrpcsvr1
    ```

## Code Quality and Maintenance

-   **Linting (using ruff):**
    ```bash
    ruff check .
    ```

-   **Formatting (using isort and ruff):**
    ```bash
    isort .
    ruff format .
    ```

-   **Type Checking (using mypy):**
    ```bash
    mypy .
    ```

-   **Type Checking (using pyright):**
    ```bash
    pyright .
    ```

## API Interaction

-   **Access Swagger UI (after server is running):**
    Open your web browser and go to `http://localhost:8000/docs`

-   **Example `curl` command for testing `sum_int` method:**
    ```bash
    curl -X POST http://127.0.0.1:8000/api \
    -H "Content-Type: application/json" \
    -d '{\
          "jsonrpc":"2.0",\
          "method":"sum_int",\
          "params":{"i":[1,2,3]},"id":1 \
        }'
    ```

## Utility Commands

Standard Linux utility commands like `git`, `ls`, `cd`, `grep`, `find` are available.