import os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.utils.azure_openai import get_embeddings


# -----------------------------
# Load documents
# -----------------------------
def load_documents():
    documents = []
    docs_path = "documents"

    for filename in os.listdir(docs_path):
        if filename.endswith(".txt"):
            with open(
                os.path.join(docs_path, filename),
                "r",
                encoding="utf-8"
            ) as f:
                documents.append(
                    Document(
                        page_content=f.read(),
                        metadata={"source": filename}
                    )
                )
    return documents


# -----------------------------
# Split documents
# -----------------------------
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)


# -----------------------------
# Create FAISS Index (Azure OpenAI)
# -----------------------------
def create_faiss_index(chunks):
    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    index_path = "app/rag/faiss_index"
    os.makedirs(index_path, exist_ok=True)
    vectorstore.save_local(index_path)

    print("✅ FAISS index created successfully using Azure OpenAI embeddings.")


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)
    create_faiss_index(chunks)
