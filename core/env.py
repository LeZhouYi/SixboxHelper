import os

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT"))

AI_URL = os.getenv("AI_URL")
AI_API_KEY = os.getenv("AI_API_KEY")
AI_AUTH_TYPE = os.getenv("AI_AUTH_TYPE")
AI_MODEL = os.getenv("AI_MODEL")

CODE_INTERPRETER_URL = os.getenv("CODE_INTERPRETER_URL")

OCR_URL = os.getenv("OCR_URL")
OCR_TYPE = os.getenv("OCR_TYPE")

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT") or 300)
