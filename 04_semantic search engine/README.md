# セマンティック検索エンジン

LangChainとChromaベクトルストアを使用したセマンティック検索エンジンの実装例です。PDFファイルから文書を読み込み、ベクトル化してセマンティック検索を可能にします。

## 機能

- **PDFファイルの読み込み**: PyPDFLoaderを使用してPDFを文書オブジェクトに変換
- **テキスト分割**: RecursiveCharacterTextSplitterで適切なサイズのチャンクに分割
- **ベクトル化**: OpenAI Embeddingsでテキストを1536次元のベクトルに変換
- **ベクトルストア**: Chromaでベクトルデータを永続化・管理
- **セマンティック検索**: 自然言語クエリで関連文書を検索

## セットアップ

### 必要なパッケージ

```bash
pip install langchain-core langchain-community langchain-openai langchain-chroma
pip install chromadb pypdf
```

### 環境変数

OpenAI APIキーを設定してください：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 使用方法

### 基本的な実行

```bash
python main.py path/to/your/pdf/file.pdf
```

### 実行手順

1. **PDFファイルの読み込み**

   - 指定されたPDFファイルをページごとに読み込み
   - 各ページが1つのDocumentオブジェクトになる

2. **テキストの分割**

   - 1000文字程度のチャンクに分割
   - 200文字のオーバーラップで文脈を保持

3. **ベクトルデータベースの構築**

   - 初回実行時にドキュメントをベクトル化してChromaに保存
   - 2回目以降は既存のデータベースを利用

4. **検索の実行**
   - 複数の検索方法でセマンティック検索を実行

### 検索の種類

#### 基本的な類似度検索

```python
results = vector_store.similarity_search("How many distribution centers does Nike have in the US?")
```

#### スコア付き検索

```python
results = vector_store.similarity_search_with_score("What was Nike's revenue in 2023?")
```

#### ベクトル検索

```python
embedding = embeddings.embed_query("How were Nike's margins impacted in 2023?")
results = vector_store.similarity_search_by_vector(embedding)
```

#### バッチ検索（LangChain Runnable）

```python
@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query)

results = retriever.batch([
    "質問1",
    "質問2",
    "質問3"
])
```

## 技術仕様

### ベクトル化モデル

- **モデル**: `text-embedding-3-small`
- **次元数**: 1536次元
- **各次元**: テキストの意味的特徴を表現する浮動小数点数(-1.0〜1.0)

### テキスト分割設定

- **チャンクサイズ**: 1000文字
- **オーバーラップ**: 200文字
- **開始位置インデックス**: 有効

### ベクトルストア設定

- **データベース**: Chroma
- **コレクション名**: `example_collection`
- **永続化ディレクトリ**: `./chroma_langchain_db`

## 注意事項

### APIレート制限

- OpenAI APIのレート制限（40,000 TPM）に注意
- 大きなPDFファイルの場合はバッチ処理で10件ずつ処理
- 処理間に1秒の待機時間を設定

### PDFエンコーディング

- 日本語PDFで`Advanced encoding /UniJIS-UTF16-H not implemented yet`の警告が表示される場合がある
- 基本的な日本語テキストは正常に処理される

### コスト管理

- 初回のベクトル化処理でOpenAI APIのコストが発生
- `main.py`内の`if False:`を`if True:`に変更してベクトル化を実行

## ファイル構成

```
04_semantic search engine/
├── main.py                 # メインプログラム
├── README.md              # このファイル
├── chroma_langchain_db/   # Chromaデータベース（自動生成）
└── nke-10k-2023.pdf      # サンプルPDFファイル
```

## 拡張方法

### 別のベクトルストア

Chroma以外のベクトルストア（Pinecone、Weaviate等）も利用可能：

```python
from langchain_pinecone import PineconeVectorStore
vector_store = PineconeVectorStore(index_name="your-index")
```

### 別の埋め込みモデル

OpenAI以外の埋め込みモデルも利用可能：

```python
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
```

## トラブルシューティング

### よくあるエラー

1. **`langchain_chroma`インポートエラー**

   ```bash
   pip install langchain-chroma
   ```

2. **レート制限エラー**

   - バッチサイズを小さくする
   - 待機時間を増やす
   - OpenAIのプランをアップグレード

3. **PDFエンコーディング警告**
   - UnstructuredPDFLoaderの使用を検討
   - PDFの再作成・変換を検討
