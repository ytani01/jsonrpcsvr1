# samples/sample2-client.py エラー表示改善計画

## 目的
`samples/sample2-client.py` におけるエラー表示を、エラー情報を損なうことなく、より見やすく、一貫性のある形式で表示するように改善する。

## 現状の課題

1.  **`requests.exceptions.ConnectionError` の処理:**
    *   エラーメッセージの文字列を手動で解析しており、出力が常に読みやすいとは限らない。
2.  **`requests.post` 中の一般的な `Exception` の処理:**
    *   エラーが発生してもユーザーに何も表示されず、デバッグが困難。
3.  **RPC エラー（`result["result"]` の `KeyError`）の処理:**
    *   `try-except KeyError` ブロックがネストしており、コードの可読性が低い。
    *   一般的な `Exception` をキャッチしており、エラー処理が不明瞭。
    *   エラー情報の表示が断片的で、構造化されたエラーデータが見にくい場合がある。

## 改善計画

1.  **エラー表示用ヘルパー関数の導入:**
    *   エラー情報（`requests.exceptions` オブジェクトまたは RPC エラー辞書）とロガーを受け取り、エラーメッセージを整形して `click.echo` で一貫して表示するヘルパー関数 `_display_error(error_data, logger)` を作成する。

2.  **`requests.exceptions.ConnectionError` 処理の改善:**
    *   `_display_error` 関数内で `requests.exceptions.ConnectionError` オブジェクトから関連情報（ホスト、ポート、理由など）を抽出し、より明確に表示するようにする。

3.  **`requests.post` 中の一般的な `Exception` 処理の改善:**
    *   `requests.post` 中に発生した `Exception` オブジェクトを `_display_error` 関数に渡し、常にユーザーにエラーが表示されるようにする。

4.  **RPC エラー処理の改善:**
    *   `_display_error` 関数内で、RPC エラーの構造（`code`, `message`, `data`）をインテリジェントに解析し、詳細なエラー情報を表示するようにする。
    *   ネストされた `try-except KeyError` ブロックを排除し、エラー処理ロジックを簡素化する。

5.  **構造化されたエラーデータの整形表示:**
    *   `err['data']` のような複雑なエラー構造を表示する際には、`json.dumps(..., indent=2)` を使用して JSON を整形出力し、可読性を向上させる。
