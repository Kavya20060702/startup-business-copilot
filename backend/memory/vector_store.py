import os
from typing import List, Dict, Any, Optional

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")

class StartupVectorStore:
    def __init__(self):
        if CHROMADB_AVAILABLE:
            os.makedirs(DB_PATH, exist_ok=True)
            self.client = chromadb.PersistentClient(path=DB_PATH)
            self.collection = self.client.get_or_create_collection(name="startup_dossiers")
        else:
            self.client = None
            self.collection = None
            self._mock_memory: List[Dict[str, Any]] = []

    def save_dossier_benchmark(self, startup_name: str, industry: str, summary: str, grade: str) -> None:
        doc_id = f"startup_{startup_name.lower().replace(' ', '_')}"
        metadata = {
            "startup_name": startup_name,
            "industry": industry,
            "investment_grade": grade
        }
        
        if CHROMADB_AVAILABLE and self.collection:
            self.collection.upsert(
                ids=[doc_id],
                documents=[summary],
                metadatas=[metadata]
            )
        else:
            self._mock_memory.append({
                "id": doc_id,
                "document": summary,
                "metadata": metadata
            })

    def search_similar_benchmarks(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        if CHROMADB_AVAILABLE and self.collection:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            parsed = []
            if results and results.get("documents"):
                docs = results["documents"][0]
                metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
                ids = results["ids"][0] if results.get("ids") else [""] * len(docs)
                for i in range(len(docs)):
                    parsed.append({
                        "id": ids[i],
                        "summary": docs[i],
                        "metadata": metas[i]
                    })
            return parsed
        else:
            # Fallback mock search
            return [
                {
                    "id": "mock_1",
                    "summary": f"[MOCK BENCHMARK] Historical analysis matching '{query}'",
                    "metadata": {"startup_name": "LogiTech AI", "industry": "Logistics", "investment_grade": "Grade A"}
                }
            ]
