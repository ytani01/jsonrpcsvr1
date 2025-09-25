# samples/sample2-client.py エラー表示改善タスクリスト

## 目的
`samples/sample2-client.py` におけるエラー表示を、エラー情報を損なうことなく、より見やすく、一貫性のある形式で表示するように改善する。

## タスク

- [x] **1. エラー表示用ヘルパー関数 `_display_error` の作成**
    - `samples/sample2-client.py` 内に、エラー情報とロガーを受け取る `_display_error(error_data, logger)` 関数を定義する。
    - この関数は、受け取った `error_data` の種類に応じて適切な形式でエラーメッセージを整形し、`click.echo` を使用して赤色で出力する責任を持つ。

- [x] **2. `requests.exceptions.ConnectionError` 処理の `_display_error` への委譲**
    - `requests.exceptions.ConnectionError` が発生した場合の `try-except` ブロックを修正し、例外オブジェクトを `_display_error` 関数に渡すようにする。
    - `_display_error` 関数内で、`ConnectionError` オブジェクトからホスト、ポート、接続拒否などの詳細情報を抽出し、ユーザーに分かりやすく表示するロジックを実装する。

- [x] **3. `requests.post` 中の一般的な `Exception` 処理の `_display_error` への委譲**
    - `requests.post` 中に発生する一般的な `Exception` をキャッチするブロックを修正し、例外オブジェクトを `_display_error` 関数に渡すようにする。
    - `_display_error` 関数内で、この一般的な例外のタイプとメッセージを適切に表示する。

- [x] **4. RPC エラー処理の `_display_error` へ の委譲と簡素化**
    - `result["result"]` の `KeyError` が発生した場合の既存の複雑な `try-except` ブロックを削除する。
    - 代わりに、RPC 応答から抽出されたエラー辞書（`result['error']`）を `_display_error` 関数に渡すようにする。
    - `_display_error` 関数内で、RPC エラー辞書（`code`, `message`, `data`）を解析し、これらの情報を構造化された形で表示するロジックを実装する。

- [x] **5. 構造化されたエラーデータの整形表示の実装**
    - `_display_error` 関数内で、RPC エラーの `data` フィールド（存在する場合）が辞書やリストなどの複雑な構造を持つ場合、`json.dumps(error_data['data'], indent=2)` を使用して整形された JSON 形式で表示するようにする。

- [x] **6. 不要なコードの削除**
    - 改善計画の実施により不要になった既存のエラー処理ロジック（特に RPC エラー処理部分のネストされた `try-except` ブロックや手動での文字列解析部分）を削除する。

- [x] **7. 必要なモジュールのインポート**
    - `json` モジュールがまだインポートされていない場合は、`json.dumps` を使用するためにインポートする。