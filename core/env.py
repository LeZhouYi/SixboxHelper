import os

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT"))

AI_URL = os.getenv("AI_URL")
AI_API_KEY = os.getenv("AI_API_KEY")

CODE_INTERPRETER_URL=os.getenv("CODE_INTERPRETER_URL")

OCR_URL = os.getenv("OCR_URL")
OCR_TYPE = os.getenv("OCR_TYPE")

REQUEST_TIMEOUT = 300