import json
from dataclasses import dataclass

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document


@dataclass
class SearchResult:
    score: float
    document: Document


class LocalVectorStore:
    def __init__(self, model_name: str):
        self.embedder = SentenceTransformer(model_name)
        self.index = None
        self.documents = []

    def _embed(self, texts: list[str]) -> np.ndarray:
        vectors = self.embedder.encode(texts, convert_to_numpy=True)
        vectors = vectors.astype("float32")
        faiss.normalize_L2(vectors)
        return vectors

    def build(self, documents: list[Document]):
        self.documents = documents
        texts = [doc.page_content for doc in documents]
        vectors = self._embed(texts)
        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(vectors)

    def search(self, query: str, k: int = 5) -> list[dict]:
        if self.index is None or not self.documents:
            return []

        qvec = self._embed([query])
        distances, indices = self.index.search(qvec, k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            score = max(0.0, 1.0 - float(dist) / 2.0)
            results.append({"score": score, "document": self.documents[idx]})
        return results

    def save(self, index_path, docstore_path):
        faiss.write_index(self.index, str(index_path))
        payload = [
            {"page_content": d.page_content, "metadata": d.metadata}
            for d in self.documents
        ]
        with open(docstore_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def load(self, index_path, docstore_path):
        self.index = faiss.read_index(str(index_path))
        with open(docstore_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        self.documents = [
            Document(page_content=item["page_content"], metadata=item["metadata"])
            for item in payload
        ]
