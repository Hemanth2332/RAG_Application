# RAG App

This app allows you to upload PDFs and ask natural language questions. It retrieves relevant document chunks using ChromaDB and augments LLM responses with grounded context.

## Features
- Batch processing of multiple PDFs in one go  
- SHA-based hashing to uniquely track uploaded documents  
- Custom chunking logic for more accurate retrieval  
- REST API built with FastAPI, optimized for validation & error handling

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Hemanth2332/RAG_Application
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

- **Example Response:**

```json
{
    "query": "What makes this architecture unique?"
    "answer": "**VGG16** stands out for its **consistent and simple structure**. It repeatedly uses the same small (3x3) convolution filters and max pool layers throughout its 16 layers. This uniform design makes it very deep and results in a large number of parameters (around 138 million).

**DenseNet-121** is unique because of its **"densely connected" design**. Instead of traditional sequential layers, every layer in a DenseNet is directly connected to all preceding layers. It achieves this by concatenating the feature maps from all previous layers and using them as input. This unique connection method allows DenseNets to be more parameter-efficient than comparable networks.",
    "context": ["1. significant number of hyper-parameters is the aspect of VGG16 that stands out the most. The number 16 in VGG16 refers to the fact that the structure is comprised....", ]
}
```

## Model & Config Notes

- **Model:** Uses Gemini 2.5 Flash model
- **Vector Store:** Embeddings are stored using Chroma DB
- **Configuration:** Update `config.py` for API keys, Models and vector DB settings.
- **Supported Formats:** PDF
---
