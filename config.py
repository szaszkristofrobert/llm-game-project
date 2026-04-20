from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
NPC_DIR = DATA_DIR / "npc"
PLAYER_DIR = DATA_DIR / "player"
RUNTIME_DIR = DATA_DIR / "runtime"
MODEL_DIR = BASE_DIR / "npc_model"

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5
SCORE_THRESHOLD = 0.7
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

USE_OLLAMA = True
OLLAMA_MODEL = "llama3.1"

INDEX_PATH = MODEL_DIR / "faiss.index"
DOCSTORE_PATH = MODEL_DIR / "documents.json"
