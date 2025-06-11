from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv("../.env")

# OpenAIモデルの初期化
model = ChatOpenAI(model="gpt-4o-mini")

# モデルに対して質問を投げる
response = model.invoke("Hello, world!")

# レスポンスを表示（テキスト部分のみ）
print(response.content)