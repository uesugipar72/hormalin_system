# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. 概要

医療機関向けの劇毒物（ホルマリン等）在庫管理デスクトップアプリケーション。

- **GUI**: Python標準の `tkinter` / `ttk` によるデスクトップアプリ（[main.py](main.py) → [gui/app.py](gui/app.py) が起点）
- **DB**: SQLite（`hormalin.db`）。スキーマ作成は [create_database.py](create_database.py)。DB接続は [utils/db_utils.py](utils/db_utils.py) の `get_connection()` に一本化（旧・重複実装の `connection.py` は削除済み）
- **配布**: PyInstaller でexe化（[main.spec](main.spec)）し `dist/` に出力
- **実行方法**: `python main.py`（DBが未作成の場合は先に `python create_database.py` を実行してテーブル・インデックス・トリガーを作成）
- ビルド/テスト/lintの自動化ツールは未整備（[requirements.txt](requirements.txt) は空、テストコードなし）。依存パッケージはコード内のimportから類推する必要がある（後述）。

主機能（ログイン → メニュー → 各画面）:
- ログイン（[gui/login_frame.py](gui/login_frame.py)）
- 入庫 / 出庫登録（[gui/stock_in_frame.py](gui/stock_in_frame.py) / [gui/stock_out_frame.py](gui/stock_out_frame.py)、実体は共通の [gui/base_transaction_frame.py](gui/base_transaction_frame.py)）
- 在庫確認（[gui/inventory_frame.py](gui/inventory_frame.py)）
- 取引履歴（[gui/history_frame.py](gui/history_frame.py)、Excel出力・カレンダー選択あり）
- 劇毒物管理簿・マスタ設定（[gui/poison_ledger_frame.py](gui/poison_ledger_frame.py)、[gui/master_frame.py](gui/master_frame.py)）は実装途中で、[gui/menu_frame.py](gui/menu_frame.py) からの導線はコメントアウトされ非表示

付随する実験的機能として、音声入力 → Whisperで文字起こし → OpenAI GPTで解析 → 在庫更新、という音声操作プロトタイプが [main_onnsei .py](main_onnsei%20.py) に存在するが、**GUI本体には未統合**（独立したエントリポイント）。

## 2. フォルダ構成

```
hormalin_system/
├── main.py                # GUI起動エントリポイント
├── main_onnsei .py         # 音声入力プロトタイプの独立エントリポイント（GUI未統合）
├── create_database.py      # DBスキーマ（テーブル/インデックス/トリガー）初期化スクリプト
├── config.py                # DBパス定義（utils/db_utils.pyのget_connection()が使用）
├── .env                     # OPENAI_API_KEY（gitignore対象、git管理外）
├── main.spec                # PyInstallerビルド設定
├── gui/                     # tkinterの各画面（Frame）
├── controllers/             # GUIとserviceを繋ぐ薄いコントローラ層
├── services/                 # DBアクセス・業務ロジック（画面に依存しない処理）
├── models/                   # DBアクセスを伴うデータモデル（在庫テーブル操作）
├── constants/                # 定数定義（入出庫アクション種別など）
├── utils/                     # 共通ユーティリティ（DB接続）
├── ui/                        # 空のCLI雛形（cli.py、未実装）
├── backup/                    # DBバックアップファイル（backup_service.pyの出力先、自動生成）
├── trash/                     # 旧GUI実装（inventory_gui.py, login_gui.py）。app.pyからは未参照、置き換え前のコード
├── build/, dist/               # PyInstallerの生成物（ビルドキャッシュ・exe本体）。手動編集しない
└── .vs/, __pycache__/          # IDE/Pythonキャッシュ。ソースではない
```

## 3. ファイル機能

### ルート
| ファイル | 機能 |
|---|---|
| [main.py](main.py) | `App()` を生成してGUIを起動するだけのエントリポイント |
| [config.py](config.py) | `DB_PATH`（`C:\DataBase\hormalin.db` 固定パス）を定義。`utils/db_utils.py` がここから読む |
| [create_database.py](create_database.py) | DB初期化用CLIスクリプト。`hormalin.db` をスクリプト直下に作成し、`chemicals`/`users`/`counterparties`/`transactions`/`inventory`/`inventory_daily_snapshot`/`poison_logs` テーブル、関連インデックス、在庫マイナス防止トリガーを作成。**`config.py` の `DB_PATH` とは別パスを独自定義しており不整合がある** |
| [main_onnsei .py](main_onnsei%20.py) | 音声録音→Whisper文字起こし→テキスト正規化→GPTでJSON解析→品目照合→在庫更新、を順に実行する音声操作プロトタイプ。`services.inventory_service.update_inventory` を呼ぶが、現行の [services/inventory_service.py](services/inventory_service.py) にはその関数が存在しない（未整合・動作しない） |
| [main.spec](main.spec) | PyInstallerビルド設定（`main.py` を単一exe化、コンソール非表示） |
| [requirements.txt](requirements.txt) | 空。実際の依存（pandas, openai, sounddevice, soundfile, numpy, openai-whisper, openpyxl, pywin32, tkcalendar 等）は各ファイルのimportから読み取る必要がある |
| [.env](.env) | `OPENAI_API_KEY` を保持。`.gitignore` で除外されておりgit管理対象外 |
| [tree.txt](tree.txt) | 過去のフォルダ構成のメモ（`database/` ディレクトリなど現状と異なる古い情報を含む。参照時は注意） |

### gui/（画面）
| ファイル | 機能 |
|---|---|
| [gui/app.py](gui/app.py) | `tk.Tk` を継承したメインウィンドウ。全Frameを生成してスタック表示し、`show_frame()` で画面切替（サイズ/リサイズ可否・`reset_form`/`refresh`/`refresh_user_display`/`reset_filters` の呼び出しもここで一括管理） |
| [gui/base_frame.py](gui/base_frame.py) | 全画面共通の基底クラス。ヘッダーにログインユーザー名を表示する `refresh_user_display()` を提供 |
| [gui/base_transaction_frame.py](gui/base_transaction_frame.py) | 入庫/出庫画面の共通実装。`action` クラス変数（"入庫"/"出庫"）でラベルや項目を出し分け、薬品・数量・部署・備考の入力フォームを構築 |
| [gui/stock_in_frame.py](gui/stock_in_frame.py) / [gui/stock_out_frame.py](gui/stock_out_frame.py) | `BaseTransactionFrame` を `action` だけ変えて継承した薄いサブクラス |
| [gui/login_frame.py](gui/login_frame.py) | ログイン画面。`services.auth_service.login()` で認証し、成功時は `controller` にユーザー情報を保存して `MenuFrame` へ遷移 |
| [gui/menu_frame.py](gui/menu_frame.py) | メイン画面。入庫/出庫/在庫確認/取引履歴への遷移ボタンとログアウト・終了ボタン（劇毒物管理簿・マスタ設定は未公開のためコメントアウト） |
| [gui/inventory_frame.py](gui/inventory_frame.py) | 在庫一覧をTreeviewで表示。`controller.inventory_controller.get_inventory_list()` から取得 |
| [gui/history_frame.py](gui/history_frame.py) | 取引履歴画面。日付/部署等でフィルタし、`services.history_service.get_history()` から取得、`openpyxl`/`win32com` でExcel出力、`tkcalendar` で日付選択 |
| [gui/poison_ledger_frame.py](gui/poison_ledger_frame.py) | 劇毒物管理簿（タブ形式、薬品種別ごとの台帳）。実装途中 |
| [gui/master_frame.py](gui/master_frame.py) | 薬品/取引先/ユーザーのマスタ設定画面。各ボタンは`print`のみで未実装 |

### controllers/ ・ models/ ・ constants/ ・ utils/
| ファイル | 機能 |
|---|---|
| [controllers/inventory_controller.py](controllers/inventory_controller.py) | `InventoryService` を保持し、`stock_in`/`stock_out`/`get_inventory_list` をGUIに薄く中継 |
| [models/inventory_model.py](models/inventory_model.py) | `inventory` テーブルへの直接アクセス（`get_quantity`/`update_quantity`） |
| [constants/inventory_constants.py](constants/inventory_constants.py) | 入出庫/廃棄のアクション種別と日本語ラベルのマッピング定数 |
| [utils/db_utils.py](utils/db_utils.py) | `get_connection()`。`sqlite3.Row` をrow_factoryに設定し列名アクセスを可能にする。**プロジェクト内で唯一のDB接続関数**（GUI/services/modelsすべてがここを経由する） |

### services/（業務ロジック・DBアクセス）
| ファイル | 機能 | GUI連携状況 |
|---|---|---|
| [services/inventory_service.py](services/inventory_service.py) | 在庫の入庫/出庫（出庫時は在庫不足チェック）、在庫一覧取得 | `InventoryController` 経由で使用中 |
| [services/auth_service.py](services/auth_service.py) | `users` テーブルでのログイン認証 | [gui/login_frame.py](gui/login_frame.py) で使用中 |
| [services/history_service.py](services/history_service.py) | `transaction_logs` を部署/薬品/ユーザーとJOINして履歴取得 | [gui/history_frame.py](gui/history_frame.py) で使用中 |
| [services/item_matcher.py](services/item_matcher.py) | `data/items.csv` とのあいまい一致（`difflib`）で品目を特定 | [main_onnsei .py](main_onnsei%20.py)専用 |
| [services/ai_parser.py](services/ai_parser.py) | OpenAI GPT-4o-miniに発話テキストを渡し、品名/動作/数量/部署のJSONを抽出 | [main_onnsei .py](main_onnsei%20.py)専用 |
| [services/recorder.py](services/recorder.py) | `sounddevice`でマイク録音し`input.wav`等に保存 | [main_onnsei .py](main_onnsei%20.py)専用 |
| [services/speech_to_text.py](services/speech_to_text.py) | Whisper(`large`モデル)で日本語音声認識 | [main_onnsei .py](main_onnsei%20.py)専用 |
| [services/speech_service.py](services/speech_service.py) | Whisper(`medium`モデル)での文字起こし。`speech_to_text.py`と機能重複 | 未呼び出し |
| [services/text_normalizer.py](services/text_normalizer.py) | 音声認識誤りの辞書置換による補正 | **内側に同名の`normalize_text`関数がネストされ未呼び出し・未`return`のバグがあり、実質何もしない** |

### trash/（旧実装、参照用）
| ファイル | 機能 |
|---|---|
| [trash/inventory_gui.py](trash/inventory_gui.py) | 旧在庫画面実装。現行`gui/`構成に置き換え済み。**`master_service`/`alert_service`をimportしていたが両方とも削除済みのため、このファイル自体は実行不可（参照用として保持）** |
| [trash/login_gui.py](trash/login_gui.py) | 旧ログイン画面実装。[gui/login_frame.py](gui/login_frame.py)に置き換え済み |

### 生成物・データ（ソースではない）
- `build/`, `dist/` — PyInstallerの中間ビルドとexe本体
- `backup/` — DBバックアップファイルの置き場（`backup_YYYYMMDD_HHMM.db`）。これらを生成していた`services/backup_service.py`は未使用のため削除済みで、現状新規ファイルは増えない
- `input.wav` — 録音テスト用の音声ファイル
- `.vs/`, `__pycache__/` — Visual StudioキャッシュとPythonバイトコードキャッシュ
