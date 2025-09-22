# Agent Notes

## 技術選定
- `app.py`でStreamlitのUIを定義.
- Pydantic v2 でデータモデルを定義.`event_tracker.models`と関連するモジュールにある.
- ネットワーク(`urllib`)、パース、永続化(JSON + filesystem)は標準ライブラリを使用.

## ディレクトリ構成
- `app.py`: UIプロトタイプ（Streamlit）のエントリーポイント.
- `event_tracker/`: fetcher, models, torage logicのPythonコード.
- `data/`: 永続化ファイルの置き場所 (JSON).
- `README.md`: プロジェクトの概要と使用上の注意点.
- `requirements.txt`: Pythonの依存関係.

## Development Notes
- - リポジトリ内のドキュメントは日本語で記述すること。
- `event_tracker/` ディレクトリ以下にモデルを追加または更新する場合は、Pydantic v2 の `BaseModel` クラスを使用することを推奨します.
- 将来的なデータベースベースのストレージ層への移行に備えてリポジトリを準備しておくとともに、ストレージ機能とユーザーインターフェース機能の間の密結合を避けるようにしてください.
