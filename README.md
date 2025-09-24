# jsonrpcsvr1: [ **WIP** (Work in Progress) ]

JSON-RPC server sample.


## 特徴

- [fastapi-jsonrpc](https://github.com/smagafurov/fastapi-jsonrpc)
  を利用しているので…

  - シンプルで拡張性が高い
  - 標準的な **JSON-RPC** で、APIを利用できる。
  - [FastAPI](https://fastapi.tiangolo.com/) と、
    [Uvicorn](https://uvicorn.dev/) により、高パフォーマンス
  - [Swagger UI](https://swagger.io/tools/swagger-ui/)が利用可能


## 利用ライブラリ

- [fastapi-jsonrpc](https://github.com/smagafurov/fastapi-jsonrpc)
- [FastAPI](https://fastapi.tiangolo.com/)


## サーバーの起動

[pyclickutils](https://github.com/ytani01/pyclickutils.git)
と
[jsonrpcsvr1](https://github.com/ytani01/jsonrpcsvr1.git)
をクローンする必要があります。

``` bash
git clone https://github.com/ytani01/pyclickutils.git
git clone https://github.com/ytani01/jsonrpcsvr1.git
cd jsonrpcsvr1
uv run jsonrpcsvr1
```


## Swagger UI による確認

Webブラウザで、APIを確認したり、動作確認することができます。

URL  http://localhost:8000/docs


## curlによる確認

コマンドラインで、`curl`コマンドを使って、動作確認することができます。

``` bash
curl -X POST http://127.0.0.1:8000/api \
-H "Content-Type: application/json" \
-d '{\
      "jsonrpc":"2.0",\
      "method":"sum_int",\
      "params":{"i":[1,2,3]},"id":1 \
    }'
```
