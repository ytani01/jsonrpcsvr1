# jsonrpcsvr1: [ **WIP** (Work in Progress) ]

JSON-RPC server sample.


## 特徴

- [fastapi-jsonrpc](https://github.com/smagafurov/fastapi-jsonrpc)
  を利用しているので…

  - シンプルで拡張性が高い
  - [FastAPI](https://fastapi.tiangolo.com/) と、
    [Uvicorn](https://uvicorn.dev/) により、高パフォーマンス
  - [Swagger UI](https://swagger.io/tools/swagger-ui/)が利用可能


## 利用ライブラリ

- [fastapi-jsonrpc](https://github.com/smagafurov/fastapi-jsonrpc)
- [FastAPI](https://fastapi.tiangolo.com/)


## サーバーの起動

``` bash
git clone https://github.com/ytani01/jsonrpcsvr1.git
cd jsonrpcsvr1
uv run jsonrpcsvr1
```


## Swagger UI

URL  http://localhost:8000/docs


## curlによる確認

``` bash
curl -X POST http://127.0.0.1:8000/api \
-H "Content-Type: application/json" \
-d '{\
      "jsonrpc":"2.0",\
      "method":"sum_int",\
      "params":{"i":[1,2,3]},"id":1 \
    }'
```
