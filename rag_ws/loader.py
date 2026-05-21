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