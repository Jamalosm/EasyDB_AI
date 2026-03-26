import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
DB_NAME = os.getenv("DB_NAME")
print("OLLAMA_URL:", OLLAMA_URL)
print("DB_NAME:", DB_NAME)  # debug