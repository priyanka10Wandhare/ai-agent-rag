# **AI Agent RAG System (FastAPI + Azure OpenAI)**

This project implements a **Retrieval-Augmented Generation (RAG) backend API** using **FastAPI**, **FAISS**, and **Azure OpenAI**.
It supports querying company documents (policies, FAQs, etc.) through a semantic search pipeline powered by embeddings and large language models.

The application is fully deployable on **Azure App Service** with **Azure OpenAI**.

---

## **Architecture Overview**

```
User Query
   |
FastAPI (/ask)
   |
Retriever (FAISS Vector Search)
   |
Top-k Relevant Documents
   |
Azure OpenAI (GPT)
   |
Final Answer + Source Documents
```

---

## **Project Structure**

```
ai-agent/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── ingest.py      # Builds FAISS index from documents
│   │   └── retriever.py   # Performs similarity search
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── azure_openai.py  # Azure OpenAI client
│
├── documents/            # Input knowledge base (TXT files)
├── requirements.txt
└── README.md
```

---

## **Azure OpenAI Configuration**

The system uses **Azure OpenAI**, not OpenAI public API.

### Required Azure resources

* Azure OpenAI resource: `openai-agent-rag`
* Embedding deployment: `embedding-model` (text-embedding-3-small)
* Chat deployment: `chat-model` (gpt-4o-mini or GPT-35)

---

## **Environment Variables**

These must be configured in **Azure App Service → Configuration → Application settings**

| Name                               |Value                                                                                    |
| ----------------------------------- | ---------------------------------------------------------------------------------------- |
| `AZURE_OPENAI_API_KEY`              | Key from Azure OpenAI resource                                                           |
| `AZURE_OPENAI_ENDPOINT`             | [https://openai-agent-rag.openai.azure.com/](https://openai-agent-rag.openai.azure.com/) |
| `AZURE_OPENAI_API_VERSION`          | 2024-07-01-preview                                                                       |
| `AZURE_OPENAI_CHAT_DEPLOYMENT`      | chat-model                                                                               |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | embedding-model                                                                          |

---

## **Install Locally**

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

---

## **Build the Vector Database**

Before running the API, documents must be embedded.

```bash
python -m app.rag.ingest
```

This creates:

```
app/rag/faiss_index/
```

---

## **Run Locally**

```bash
python -m uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## **API Usage**

### Endpoint

```
POST /ask
```

### Request

```json
{
  "query": "What is the leave policy?",
  "session_id": "user1"
}
```

### Response

```json
{
  "answer": "Employees are entitled to 20 paid leaves per year...",
  "source": ["leave_policy.txt"]
}
```

---

## **Azure Deployment**

### Startup Command (App Service → Configuration → General)

```
gunicorn --chdir /home/site/wwwroot/ai-agent app.main:app --workers 2 --timeout 120
```

---

## **Public API URL**

```
https://agent-openai-rag-e2hkcsfzbfekf9fz.centralindia-01.azurewebsites.net
```

Swagger:

```
/docs
```

---

## **Technologies Used**

* FastAPI
* FAISS
* LangChain
* Azure OpenAI
* Gunicorn
* Azure App Service

---

## **Assignment Compliance**

| Requirement          | Status |
| -------------------- | ------ |
| RAG using embeddings | ✅      |
| FAISS Vector DB      | ✅      |
| Azure OpenAI         | ✅      |
| FastAPI backend      | ✅      |
| Azure deployment     | ✅      |
| Public API           | ✅      |

---

## **Author**

Priyanka Wandhare
