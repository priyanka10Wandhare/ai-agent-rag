import numpy as np
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS

# -----------------------------
# Proper Mock Embeddings Class
# -----------------------------
class MockEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [np.random.rand(1536).tolist() for _ in texts]

    def embed_query(self, text):
        return np.random.rand(1536).tolist()

# -----------------------------
# Load FAISS Vector Store
# -----------------------------
def load_vectorstore():
    embeddings = MockEmbeddings()
    vectorstore = FAISS.load_local(
        "app/rag/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore

# -----------------------------
# Retrieve Documents
# -----------------------------
def retrieve(query: str, k: int = 3):
    vectorstore = load_vectorstore()
    return vectorstore.similarity_search(query, k=k)

# -----------------------------
# Test Run
# -----------------------------
if __name__ == "__main__":
    query = "What is the company leave policy?"
    docs = retrieve(query)

    print("\n🔍 Retrieved Documents:\n")
    for i, doc in enumerate(docs, 1):
        print(f"--- Result {i} ---")
        print(doc.page_content[:400])
        print("Source:", doc.metadata.get("source"))
        print()
