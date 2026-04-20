from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    DATA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DOCSTORE_PATH,
    EMBED_MODEL_NAME,
    INDEX_PATH,
    MODEL_DIR,
)
from vector_store import LocalVectorStore



def infer_type(file_name: str) -> str:
    lower = file_name.lower()
    if "szemelyiseg" in lower:
        return "szemelyiseg"
    if "feladas" in lower:
        return "feladas"
    if "jatekos" in lower:
        return "jatekos"
    return "unknown"



def load_static_documents() -> list[Document]:
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    raw_docs = loader.load()

    filtered_docs = []
    for doc in raw_docs:
        src = Path(doc.metadata.get("source", ""))
        if "runtime" in src.parts:
            continue

        metadata = {
            "source": str(src),
            "type": infer_type(src.name),
            "npc": None,
        }
        filtered_docs.append(Document(page_content=doc.page_content, metadata=metadata))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(filtered_docs)


if __name__ == "__main__":
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    docs = load_static_documents()
    store = LocalVectorStore(EMBED_MODEL_NAME)
    store.build(docs)
    store.save(INDEX_PATH, DOCSTORE_PATH)
    print(f"Index kész: {INDEX_PATH}")
    print(f"Dokumentumok száma: {len(docs)}")
