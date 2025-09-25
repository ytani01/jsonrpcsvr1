# GEMINI.md

Gemini CLI のための開発ルール。

## == serena MCP server

``` text
@serena activate current directory
@serena onboarding
@serena switch_mode ["planning", "one-shot"]
@serena switch_mode ["editing", "interactive"]
@serena think_about_whether_you_are_done
```


## == プロジェクトについて

- JSON-RPC server sample.

- [fastapi-jsonrpc](https://github.com/smagafurov/fastapi-jsonrpc)
  を利用しているので…

  - シンプルで拡張性が高い
  - 標準的な **JSON-RPC** で、APIサーバーを作成・利用できる。
  - [FastAPI](https://fastapi.tiangolo.com/) と、
    [Uvicorn](https://uvicorn.dev/) により、高パフォーマンス
  - [Swagger UI](https://swagger.io/tools/swagger-ui/)が利用可能
