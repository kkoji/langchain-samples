from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv("../.env")


model = ChatOpenAI(model="gpt-4o-mini")

# メッセージを作成
messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi! Nice to meet you! I'm John."),
]

# ユーザーメッセージ送信方法として以下は全て同等
# model.invoke("Hello")
# model.invoke([{"role": "user", "content": "Hello!"}])
# model.invoke([HumanMessage("Hello!")])

# レスポンスを一括で受け取る場合の呼び出し方
response = model.invoke(messages)
print(response.content)

# ストリーミングでレスポンスを受け取る場合の呼び出し方
for token in model.stream(messages):
    print(token.content, end="|")