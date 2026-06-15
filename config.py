from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
GODOT_DIR = BASE_DIR / "godot"
RUNTIME_DIR = GODOT_DIR / "runtime"
MODEL_DIR = BASE_DIR / "npc_model"

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5
SCORE_THRESHOLD = 0.035
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

USE_OLLAMA = True
OLLAMA_MODEL = "llama3.1:8b"

INDEX_PATH = MODEL_DIR / "faiss.index"
DOCSTORE_PATH = MODEL_DIR / "documents.json"
