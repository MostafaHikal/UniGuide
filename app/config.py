import os
from dotenv import load_dotenv

load_dotenv()


# =========================
# LLM
# =========================
MODEL_NAME      = os.getenv("MODEL_NAME")
GROQ_API_KEY    = os.getenv("GROQ_API_KEY")
VISION_MODEL    = os.getenv("VISION_MODEL_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")


# =========================
# PATHS
# =========================
VECTOR_STORE_PATH = "vector_store/faiss_index"
TABLES_JSON_PATH  = "data/tables.json"
POPPLER_PATH      = r"D:\Release-26.02.0-0\poppler-26.02.0\Library\bin"


# =========================
# RETRIEVAL
# =========================
RAG_TOP_K       = 15
RAG_FETCH_K     = 40
FUZZY_THRESHOLD = 75


# =========================
# INGESTION
# =========================
CHUNK_SIZE    = 800
CHUNK_OVERLAP = 200
OCR_DPI       = 400
OCR_LANG      = "ara+eng"