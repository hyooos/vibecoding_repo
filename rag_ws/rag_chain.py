from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sbert-nli"
)

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

from langchain_core.prompts import PromptTemplate

template = """
다음 문서를 참고해서 질문에 답하세요.

문서:
{context}

질문:
{question}

답변:
"""

prompt = PromptTemplate.from_template(template)

from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough
)

def format_docs(docs):
    return "\n\n".join(
        doc.page_content for doc in docs
    )

chain = (
    {
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough(),
    }
    | prompt
)

question = "인공지능은 어디에 사용되나요?"
prompt_value = chain.invoke(question)

print(prompt_value.to_string())

from langchain_huggingface import HuggingFacePipeline
from langchain_core.output_parsers import StrOutputParser

llm = HuggingFacePipeline.from_model_id(
    model_id="Qwen/Qwen2.5-0.5B-Instruct",
    task="text-generation",
    pipeline_kwargs={
        "max_new_tokens": 256,
        "return_full_text": False,
        "do_sample": False,
    },
)

full_chain = chain | llm | StrOutputParser()

answer = full_chain.invoke(question)

print(answer)