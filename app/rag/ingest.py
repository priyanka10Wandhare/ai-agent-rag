import os
import numpy as np
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# -----------------------------
# Mock Embedding Class
# -----------------------------
class MockEmbeddings:
    def embed_documents(self, texts):
        # Create deterministic fake vectors
        return [np.random.rand(1536).tolist() for _ in texts]

    def embed_query(self, text):
        return np.random.rand(1536).tolist()

# -----------------------------
# Load documents
# -----------------------------
def load_documents():
    documents = []
    docs_path = "documents"

    for filename in os.listdir(docs_path):
        if filename.endswith(".txt"):
            with open(os.path.join(docs_path, filename), "r", encoding="utf-8") as f:
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
# Create FAISS Index
# -----------------------------
def create_faiss_index(chunks):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs("app/rag/faiss_index", exist_ok=True)
    vectorstore.save_local("app/rag/faiss_index")

    print("✅ Mock FAISS index created successfully.")

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)
    create_faiss_index(chunks)
