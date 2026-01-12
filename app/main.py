from fastapi import FastAPI
from app.rag.retriever import retrieve

app = FastAPI()

@app.post("/ask")
def ask(payload: dict):
    query = payload.get("query")
    session_id = payload.get("session_id")

    docs = retrieve(query)
    answer = docs[0].page_content if docs else "No answer found"

    return {
        "answer": answer,
        "source": [d.metadata.get("source", "unknown") for d in docs]
    }
