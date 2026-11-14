import os
from dotenv import load_dotenv

load_dotenv()


class config:
    GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/openai"
    GEMINI_CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL", "gemini-3.8-flash")
    GEMINI_EMBEDDING_MODEL = os.getenv(
        "GEMINI_EMBEDDING_MODEL", "gemini-embedding-001"
    )
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
    VECTOR_DB_PATH = "vector_db"

    @classmethod
    def require_gemini_api_key(cls):
        if not cls.GEMINI_API_KEY:
            raise RuntimeError(
                "Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment or .env file."
            )
        return cls.GEMINI_API_KEY