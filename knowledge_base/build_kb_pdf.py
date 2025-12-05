import os
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

def chunk_text(text, chunk_size=800):
    # simple chunking
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def build_kb():
    print("[1] Loading PDF...")
    pdf = PdfReader("Treatment-of-Common-Dermatologic-Conditions.pdf")

    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"

    chunks = chunk_text(text)
    print("[2] Total Chunks:", len(chunks))

    print("[3] Loading Embedder...")
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    print("[4] Creating Chroma DB...")
    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_or_create_collection(
        name="derm_kb",
        metadata={"hnsw:space": "cosine"}
    )

    # embeddings
    embeddings = embedder.encode(chunks, batch_size=16, show_progress_bar=True)

    print("[5] Storing chunks...")
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings
    )

    print("[✓] Done building dermatology knowledge base!")

if __name__ == "__main__":
    build_kb()
