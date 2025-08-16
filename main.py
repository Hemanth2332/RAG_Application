from fastapi import FastAPI, UploadFile, File, HTTPException
from ingestion import ingest_pdf
from retrieval import get_relevant_contents, make_prompt
from gemini_service import ask_gemini
import tempfile, os, uuid, logging
from schema import QueryRequest


app = FastAPI(title="RAG PDF QA Bot")
DOC_STORE = {}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and ingest a PDF into ChromaDB. Returns a document_id for later queries.
    """

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        
        db, db_name = ingest_pdf(tmp_path)
  
        document_id = str(uuid.uuid4())
        DOC_STORE[document_id] = db

        
        os.remove(tmp_path)
        return {"message": "PDF ingested successfully", "document_id": document_id}

    except Exception as e:
        logging.error(f"Error in upload_pdf: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to ingest PDF: {str(e)}")


@app.post("/query/")
async def query_document(request: QueryRequest):
    """
    Query an ingested PDF using the document_id returned at upload time.
    """

    if request.document_id not in DOC_STORE:
        raise HTTPException(status_code=404, detail=f"Document {request.document_id} not found. Please upload first.")

    try:
        db = DOC_STORE[request.document_id]

        
        passages = get_relevant_contents(request.query, db, k=3)
        if not passages:
            raise HTTPException(status_code=404, detail="No relevant passages found in the document")

        logging.info(f"Retrieved {len(passages)} passages for query '{request.query}'")

        
        prompt = make_prompt(request.query, passages[0])
        answer = ask_gemini(prompt)

        return {
            "query": request.query,
            "answer": answer,
            "context": passages
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in query_document: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")