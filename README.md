# RAG App

A Retrieval-Augmented Generation (RAG) application for document upload and querying using LLMs.

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/rag_app.git
    cd rag_app
    ```

2. **Create a virtual environment & activate:**

    **Using pip:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

    **Using uv:**
    ```bash
    uv init
    ```

3. **Install dependencies:**
    
    **Using pip:**
    ```bash
    pip install -r requirements.txt
    ```

    **Using uv:**
    ```bash
      uv sync --frozen --no-cache
    ```

## Run

Start the application:
```bash
uvicorn main:app --port 8000 --reload
```
The server will run on `http://localhost:8000` by default.

## API Usage

### 1. Upload Documents

- **Endpoint:** `POST /upload`
- **Description:** Upload a document for indexing.
- **Request:**
  - Content-Type: `multipart/form-data`
  - Field: `file` (the document to upload)
- **Example (using `curl`):**
  ```bash
  curl -F "file=@yourfile.pdf" http://localhost:8000/upload
  ```
- **Response:**
    ```bash
    {
        "status" : "success",
        "document_id" : "<document_id>"
    }

### 2. Query

- **Endpoint:** `POST /query`
- **Description:** Query the indexed documents using natural language.
- **Request:**
  - Content-Type: `application/json`
  - Body: `{ "question": "Your question here" }`
- **Example:**
  ```bash
  curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"question": "What is RAG?", "document_id": "<document_id>}'
  ```

## Model & Config Notes

- **Model:** Uses a local or cloud-hosted LLM (e.g., OpenAI, HuggingFace Transformers).
- **Vector Store:** Embeddings are stored using Chroma DB
- **Configuration:** Update `config.py` for model endpoints, API keys, and vector DB settings.
- **Supported Formats:** PDF
---
