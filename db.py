import chromadb
import time, random
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from google import genai
from google.genai.errors import ClientError
from google.genai import types
from config import GEMINI_API_KEY, EMBEDDING_MODEL_ID, DB_BASE_PATH
import os


client = genai.Client(api_key=GEMINI_API_KEY)

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        if isinstance(input, str):
            input = [input]
        retries = 3
        for attempt in range(retries):
            try:
                response = client.models.embed_content(
                    model=EMBEDDING_MODEL_ID,
                    contents=input,
                    config=types.EmbedContentConfig(task_type="retrieval_document")
                )
                return [emb.values for emb in response.embeddings]
            except ClientError as e:
                if "RESOURCE_EXHAUSTED" in str(e) and attempt < retries - 1:
                    sleep_time = 2 ** attempt + random.random()
                    print(f"⚠️ Rate limit. Retry in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                else:
                    raise

def get_db_path(db_name: str) -> str:
    return os.path.join(DB_BASE_PATH, db_name)


def create_chroma_db(documents, name, batch_size=50): #change this to 10 if not working properly
    db_path = get_db_path(name)
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(
        name=name,
        embedding_function=GeminiEmbeddingFunction()
    )
    if collection.count() == 0:
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            ids = [str(j) for j in range(i, i+len(batch_docs))]
            collection.add(documents=batch_docs, ids=ids)
    return collection


