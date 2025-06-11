# ChatPromptTemplate を使ったプロンプトテンプレート

このサンプルは、LangChainの`ChatPromptTemplate`を使ってプレースホルダー付きのプロンプトテンプレートを作成し、動的に値を埋め込む方法を示しています。

## 機能

- OpenAI APIキーの環境変数読み込み（`.env`ファイルから）
- ChatOpenAIモデル（gpt-4o-mini）の初期化
- `ChatPromptTemplate.from_messages()`を使ったプロンプトテンプレートの作成
- システムメッセージとユーザーメッセージの組み合わせ
- プレースホルダー（`{language}`, `{text}`）を使った動的な値の埋め込み
- `invoke()`メソッドを使った実際のプロンプト生成とAIモデルでの実行

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
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv("../.env")

# OpenAIモデルの初期化
model = ChatOpenAI(model="gpt-4o-mini")

# 複数のプロンプトを作成する場合は、以下のようにする
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from English into {language}"),
    ("user", "{text}")
])

# プレースホルダーに値を代入してプロンプトを作成
prompt = prompt_template.invoke({
    "language": "Japanese",
    "text": "Hello, how are you?"
})

print("prompt:", prompt)
print("response:", model.invoke(prompt).content)
```

## 期待される出力

生成されたプロンプトオブジェクトと翻訳結果が表示されます：

```
prompt: messages=[SystemMessage(content='Translate the following from English into Japanese'), HumanMessage(content='Hello, how are you?')]
response: こんにちは、元気ですか？
```

## ポイント

- **プロンプトテンプレート**: 再利用可能なプロンプトの雛型を作成
- **プレースホルダー**: `{変数名}`形式で動的な値を埋め込み可能
- **メッセージタイプ**: `"system"`, `"user"`, `"assistant"`などを指定可能
- **invoke()メソッド**: 辞書形式でプレースホルダーに値を代入してプロンプトを生成
- **再利用性**: 同じテンプレートで異なる言語やテキストに対応可能

## 応用例

このテンプレートを使えば、以下のような応用が可能です：

```python
# 異なる言語への翻訳
italian_prompt = prompt_template.invoke({
    "language": "Italian",
    "text": "Good morning!"
})

# 異なるテキストの翻訳
french_prompt = prompt_template.invoke({
    "language": "French",
    "text": "How are you?"
})

# 実際に翻訳を実行
print("Italian:", model.invoke(italian_prompt).content)
print("French:", model.invoke(french_prompt).content)
```
