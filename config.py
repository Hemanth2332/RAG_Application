import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
GEMINI_API_KEY = os.getenv("GENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID")
DB_BASE_PATH = os.getenv("DB_BASE_PATH", "./db")
