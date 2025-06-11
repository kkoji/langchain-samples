# マルチメッセージ翻訳プロンプト

このサンプルは、LangChainでSystemMessageとHumanMessageを組み合わせて翻訳タスクを実行する例です。システムメッセージでタスク指示を行い、ユーザーメッセージで翻訳対象のテキストを送信します。

## 機能

- SystemMessageによる翻訳タスクの指示（英語→イタリア語）
- HumanMessageによる翻訳対象テキストの送信
- マルチメッセージプロンプトの構成方法
- OpenAI APIキーの環境変数読み込み（`.env`ファイルから）
- ChatOpenAIモデル（gpt-4o-mini）を使った翻訳実行

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

# メッセージリストを作成
messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]

# マルチメッセージプロンプトを実行
response = model.invoke(messages)
print(response.content)
```

## 期待される出力

英語の「hi!」がイタリア語に翻訳された結果が表示されます（例：「Ciao!」など）。

## ポイント

- **SystemMessage**: AIに対するタスク指示や役割設定に使用
- **HumanMessage**: ユーザーからの実際の質問や入力に使用
- メッセージの順序が重要：SystemMessageを先に配置することで、AIに明確な指示を与える
- 複数のメッセージを組み合わせることで、より構造化されたプロンプトを作成可能
