import time
from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Documentオブジェクトを直接作成する場合のサンプル
# documents = [
#     Document(
#         page_content="犬は忠誠心と友好性で知られ、素晴らしい仲間です。",
#         metadata={"source": "mammal-pets-doc"},
#     ),
#     Document(
#         page_content="猫は独立心旺盛なペットで、自分の空間を楽しむことが多いです。",
#         metadata={"source": "mammal-pets-doc"},
#     ),
# ]

# PyPDFLoaderを使ってPDFファイルのメタ情報、コンテンツをロードしてDocumentオブジェクトのlistを作成
loader = PyPDFLoader("./04_semantic search engine/nke-10k-2023.pdf")
docs = loader.load()
# 1ページ当たり1Documentオブジェクトが作成されるので docsの数 = PDF数 となる
print(f"PDFのページ数: {len(docs)}")
# print(f"1ページ目の先頭100文字: {docs[0].page_content[:100]}")
# print(f"1ページ目のメタ情報: {docs[0].metadata}")

# 概ね1000文字に分割し、分割したドキュメントごとに200文字の重複を許容する
# （自然な区切り位置で分割するので必ずしも1000文字未満の場合もある）
# add_start_index=True は分割したドキュメントごとに,分割したドキュメントの開始位置を付与するためのオプション
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
all_splits = text_splitter.split_documents(docs)
print(f"分割後のドキュメント数: {len(all_splits)}")
print(f"分割後の1ページ目の文字数: {len(all_splits[0].page_content)}")
print(f"分割後の1ページ目のドキュメントのインデックス: {all_splits[0].metadata['start_index']}")
print(f"分割後の2ページ目のドキュメントのインデックス: {all_splits[1].metadata['start_index']}\n")

db_path = "./04_semantic search engine/chroma_langchain_db"
# このモデルの場合は1536次元のベクトルが生成される
# - これが理由で各ドキュメントに対するembed_queryの結果が1536個の要素の配列になる
# - 各要素の値は潜在的特徴を表す数値で人間が呼んで意味のある値ではない
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Chroma（vector_store）のインスタンスを生成
# dbファイルが存在する場合はembedせずにファイルを読み取ってvector_storeを作成
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory=db_path,
)
# 試しに1ページ目と2ページ目のドキュメントをembeddingsする場合のコード
# vector_1 = embeddings.embed_query(all_splits[0].page_content)
# vector_2 = embeddings.embed_query(all_splits[1].page_content)
# assert len(vector_1) == len(vector_2)


if False: # OpenAIのAPI費用がかかるのでベクトルDBに保存する場合のみ有効化
    # Chromaにドキュメントを追加
    # all_splitsを全件追加する
    print(f"ドキュメントを追加します...")

    # レートリミットを避けるために10件ずつドキュメントを追加
    batch_size = 10
    all_ids = []
    for i in range(0, len(all_splits), batch_size):
        batch = all_splits[i:i + batch_size]
        batch_ids = vector_store.add_documents(documents=batch)
        all_ids.extend(batch_ids)
        print(f"{i + len(batch)}/{len(all_splits)}件追加完了")
        time.sleep(1)
    ids = all_ids
    print(f"ドキュメントの追加結果: {ids}")

# 以下はベクトルDBで検索する際のバリエーションのサンプル

# vector storeのDBに対してクエリを投げて関連するする箇所を取得
results = vector_store.similarity_search("How many distribution centers does Nike have in the US?")
print(f"検索結果の数: {len(results)}")
print(f"検索結果: {results[0]}\n")

# 次のメソッドではスコアも取得できる
# スコアはプロバイダーによって算出方法が異なるので注意
results = vector_store.similarity_search_with_score("What was Nike's revenue in 2023?")
doc, score = results[0]
print(f"スコア: {score}\n")

# 検索ワードをembeddingして検索するケース
embedding = embeddings.embed_query("How were Nike's margins impacted in 2023?")
results = vector_store.similarity_search_by_vector(embedding)
print(f"検索結果: {results[0]}\n")

# 以下はvectore_storeをRunableに変換するサンプル
# 以下のようにすると、retriever経由でinvokeやbatchといったメソッドが使えるようになり、LangChainの処理でチェーンできるようになる
@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query)

results = retriever.batch([
    "How many distribution centers does Nike have in the US?",
    "What was Nike's revenue in 2023?",
    "How were Nike's margins impacted in 2023?",
])
print(f"検索結果: {results[0]}\n")