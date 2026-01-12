from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict

from app.rag.retriever import retrieve
from app.memory.memory import ConversationMemory

# -----------------------------
# App Initialization
# -----------------------------
app = FastAPI(title="RAG Backend API")

# Session-based memory store
sessions: Dict[str, ConversationMemory] = {}

# -----------------------------
# Mock LLM
# -----------------------------
class MockLLM:
    def generate(self, prompt: str) -> str:
        return (
            "Based on the available documents, here is the answer:\n\n"
            + prompt[:500]
        )

# -----------------------------
# Request / Response Models
# -----------------------------
class AskRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"

class AskResponse(BaseModel):
    answer: str
    source: List[str]

# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    session_id = request.session_id

    if session_id not in sessions:
        sessions[session_id] = ConversationMemory()

    memory = sessions[session_id]
    memory.add_user_message(request.query)

    docs = retrieve(request.query, k=3)

    sources = list(set(doc.metadata.get("source") for doc in docs))

    context = "\n\n".join(
        f"Source: {doc.metadata.get('source')}\n{doc.page_content}"
        for doc in docs
    )

    prompt = f"""
Conversation History:
{memory.get_context()}

Document Context:
{context}

Question:
{request.query}

Answer:
"""

    llm = MockLLM()
    answer = llm.generate(prompt)

    memory.add_ai_message(answer)

    return {
        "answer": answer,
        "source": sources
    }
