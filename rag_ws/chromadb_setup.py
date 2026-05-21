from langchain_community.document_loaders import TextLoader, DirectoryLoader

# ─── 1. 단일 파일 로드 ─────────────────────────────
loader = TextLoader('sample_docs/sample1.txt', encoding='utf-8')
docs = loader.load()

print(f'[TextLoader] 문서 수: {len(docs)}')
print(f'글자 수: {len(docs[0].page_content)}')
print(f'메타데이터: {docs[0].metadata}')

# ─── 2. 폴더 전체 로드 ─────────────────────────────
dir_loader = DirectoryLoader(
    'sample_docs/',
    glob='**/*.txt',
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}
)

all_docs = dir_loader.load()

print(f'[DirectoryLoader] 총 문서 수: {len(all_docs)}')

from langchain_text_splitters import RecursiveCharacterTextSplitter

# ─── 3. 텍스트 분할 ─────────────────────────────
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
    separators=["\n\n", "\n", " "],
)

chunks = splitter.split_documents(all_docs)

print(f'총 청크 수: {len(chunks)}')
print(f'첫 번째 청크:')
print(chunks[0].page_content)
print(f'메타데이터: {chunks[0].metadata}')

# 문서별 chunk 개수 확인하기
for i, doc in enumerate(all_docs):
    split_docs = splitter.split_documents([doc])

    print(f'\n[sample{i+1}]')
    print(f'청크 수: {len(split_docs)}')

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sbert-nli"
)

query_vector = embeddings.embed_query(
    "인공지능은 어디에 사용되나요?"
)

print(len(query_vector))
print(query_vector[:5])

import os
from langchain_chroma import Chroma

if not os.path.exists("./chroma_db"):
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db",
    )
    print("ChromaDB 새로 저장 완료")
else:
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings,
    )
    print("기존 ChromaDB 불러오기 완료")

print(f"저장된 청크 수: {len(chunks)}")

query = "인공지능은 어디에 사용되나요?"
results = vectorstore.similarity_search(query, k=2)

print("\n[유사도 검색 결과]")

for i, doc in enumerate(results, start=1):
    print(f"\n--- 결과 {i} ---")
    print(doc.page_content)
    print(doc.metadata)