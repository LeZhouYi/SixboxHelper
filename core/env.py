import os

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT"))
AI_HOST = os.getenv("AI_HOST")
AI_MODEL = os.getenv("AI_MODEL")

AI_URL = os.getenv("AI_URL")
AI_API_KEY = os.getenv("AI_API_KEY")

CODE_INTERPRETER_URL=os.getenv("CODE_INTERPRETER_URL")