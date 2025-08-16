import hashlib
from db import create_chroma_db
from PyPDF2 import PdfReader
# import fitz


def read_pdf(file_path: str) -> str:
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        return "\n".join([p.extract_text() or "" for p in reader.pages])

# pymupdf alternative

# def read_pdf(file_path: str) -> str:
#     doc = fitz.open(file_path)
#     text = []
#     for page in doc:
#         text.append(page.get_text("text"))  # extract plain text
#     doc.close()
#     return "\n".join(text)

def chunk_text(text: str, chunk_size=300, overlap=50):
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += max(1, chunk_size - overlap)
    return chunks



def compute_file_hash(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()[:16]


def ingest_pdf(file_path: str):
    file_hash = compute_file_hash(file_path)
    db_name = f"pdf_{file_hash}"
    text = read_pdf(file_path)
    chunks = chunk_text(text)
    db = create_chroma_db(chunks, db_name)
    return db, db_name