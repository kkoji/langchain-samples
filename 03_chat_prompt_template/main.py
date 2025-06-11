from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv("../.env")


model = ChatOpenAI(model="gpt-4o-mini")

# 複数のプロンプトを作成する場合は、以下のようにする
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from English into {language}"),
    ("user", "{text}")
])

# プレースホルダーに値を代入してプロンプトを作成（実際にはチャットボットなどのアプリケーションへの入力値を埋め込む）
prompt = prompt_template.invoke({
    "language": "Japanese",
    "text": "Hello, how are you?"
})

print("prompt:", prompt)

print("response:", model.invoke(prompt).content)