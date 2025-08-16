from google import genai
from config import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str):
    return client.models.generate_content(model=MODEL_NAME, contents=prompt).text
