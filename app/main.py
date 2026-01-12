from app.rag.retriever import retrieve

# -----------------------------
# Mock LLM
# -----------------------------
class MockLLM:
    def generate(self, prompt: str) -> str:
        return (
            "Based on the provided documents, here is a summary:\n\n"
            + prompt[:600]
            + "\n\n(Note: This response was generated using a mock LLM.)"
        )

# -----------------------------
# RAG Pipeline
# -----------------------------
def rag_answer(question: str) -> str:
    docs = retrieve(question, k=3)

    context = "\n\n".join(
        f"Source: {doc.metadata.get('source')}\n{doc.page_content}"
        for doc in docs
    )

    prompt = f"""
You are an AI assistant. Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}

Answer:
"""

    llm = MockLLM()
    return llm.generate(prompt)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    question = "What is the company leave policy?"
    answer = rag_answer(question)

    print("\n🤖 RAG Answer:\n")
    print(answer)
