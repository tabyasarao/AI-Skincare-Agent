import os
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # project/
DB_PATH = os.path.join(BASE_DIR, "knowledge_base", "chroma_db")

# Load embedder
embedder = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

# NEW Chroma Client
client = chromadb.PersistentClient(path=DB_PATH)

# Load vector collection
collection = client.get_or_create_collection(name="derm_kb")


def rag_agent(query):
    print("[RAG Agent] Retrieving dermatology evidence...")

    query_emb = embedder.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=3
    )
    
    docs = results.get("documents", [[]])[0]
    
    if not docs:
        return ["No related clinical evidence found in dermatology PDF."]
    
    return docs


# ---- TEST ----
if __name__ == "__main__":
    print("=== TEST: RAG Search Agent ===")
    out = rag_agent("acne treatment recommendations")

    print("\nRetrieved Evidence:")
    for i, chunk in enumerate(out, start=1):
        print(f"\n--- Chunk #{i} ---")
        print(chunk)
