# 基本的なモデル初期化と実行

このサンプルは、LangChainを使ってOpenAIのChatGPTモデルを初期化し、基本的な対話を行う最もシンプルな例です。

## 機能

- OpenAI APIキーの環境変数読み込み（`.env`ファイルから）
- ChatOpenAIモデル（gpt-4o-mini）の初期化
- 基本的なメッセージ送信とレスポンス受信

## 実行方法

1. ルートディレクトリに`.env`ファイルを作成し、OpenAI APIキーを設定：

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

2. 必要なパッケージをインストール：

   ```bash
   python3 -m venv venv
   pip install -r requirements.txt
   ```

3. スクリプトを実行：
   ```bash
   python main.py
   ```

## コード概要

```python
# .envファイルから環境変数を読み込み
load_dotenv("../.env")

# OpenAIモデルの初期化
model = ChatOpenAI(model="gpt-4o-mini")

# モデルに対して質問を投げる
response = model.invoke("Hello, world!")

# レスポンスを表示（テキスト部分のみ）
print(response.content)
```

## 期待される出力

モデルからの挨拶の返答が表示されます（例：「Hello! How can I assist you today?」など）。
