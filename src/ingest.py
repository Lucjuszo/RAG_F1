import re
from pathlib import Path
import fitz  # pymupdf
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich.console import Console
from rich.progress import track
import uuid

QDRANT_URL      = "http://localhost:6333"
COLLECTION_NAME = "f1_drivers"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_SIZE     = 384

CHUNK_SIZE      = 800
CHUNK_OVERLAP   = 100

PDFS_DIR        = Path(__file__).parent.parent / "data" / "pdfs"

console = Console()

def filename_to_driver(filename: str):
    """'Lewis_Hamilton.pdf' -> 'Lewis Hamilton'"""
    return Path(filename).stem.replace("_", " ")

def extract_text_from_pdf(pdf_path: Path):
    doc = fitz.open(pdf_path)
    pages = [page.get_text() for page in doc]
    return "\n".join(pages)

def load_pdfs(pdfs_dir: Path):
    docs = []
    for path in sorted(pdfs_dir.glob("*.pdf")):
        text = extract_text_from_pdf(path)
        driver = filename_to_driver(path.name)
        docs.append({
            "filename": path.name,
            "driver":   driver,
            "text":     text,
        })
        console.print(f"  Done: {driver} ({len(text)} characters)")
    return docs

def split_into_chunks(docs: list[dict]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = []
    for doc in docs:
        parts = splitter.split_text(doc["text"])
        for i, part in enumerate(parts):
            chunks.append({
                "id":          str(uuid.uuid4()),
                "text":        part,
                "driver":      doc["driver"],
                "filename":    doc["filename"],
                "chunk_index": i,
            })
    return chunks

def setup_collection(client: QdrantClient):
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in existing:
        console.print(f"[yellow]Info:[/yellow] Collection '{COLLECTION_NAME}' exists - deleting.")
        client.delete_collection(COLLECTION_NAME)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    console.print(f"[green]Done:[/green] Collection '{COLLECTION_NAME}' created.")

def embed_and_upload(chunks: list[dict], client: QdrantClient, model: SentenceTransformer):
    texts   = [c["text"] for c in chunks]
    console.print("\n[bold]Generating embeddings...[/bold]")
    vectors = model.encode(texts, show_progress_bar=True, batch_size=32)

    points = [
        PointStruct(
            id=chunk["id"],
            vector=vector.tolist(),
            payload={
                "text":        chunk["text"],
                "driver":      chunk["driver"],
                "filename":    chunk["filename"],
                "chunk_index": chunk["chunk_index"],
            },
        )
        for chunk, vector in zip(chunks, vectors)
    ]

    batch_size = 100
    for i in track(range(0, len(points), batch_size), description="Uploading to Qdrant..."):
        client.upsert(collection_name=COLLECTION_NAME, points=points[i:i + batch_size])

    console.print(f"[green]Done:[/green] Uploaded {len(points)} chunks to Qdrant.")

def main():
    console.rule("[bold blue]F1 RAG - Ingest Pipeline[/bold blue]")

    console.print("\n[bold]1. Loading PDFs...[/bold]")
    docs = load_pdfs(PDFS_DIR)
    if not docs:
        console.print("[red]No PDFs found in data/pdfs/![/red]")
        return

    console.print("\n[bold]2. Chunking...[/bold]")
    chunks = split_into_chunks(docs)
    console.print(f"   Total chunks: [cyan]{len(chunks)}[/cyan]")

    console.print("\n[bold]3. Loading embedding model...[/bold]")
    model = SentenceTransformer(EMBEDDING_MODEL)

    console.print("\n[bold]4. Connecting to Qdrant...[/bold]")
    client = QdrantClient(url=QDRANT_URL)
    setup_collection(client)

    console.print("\n[bold]5. Embeddings and upload...[/bold]")
    embed_and_upload(chunks, client, model)

    console.rule("[bold green]Ingest completed![/bold green]")
    console.print(f"   Drivers: {len(docs)}")
    console.print(f"   Chunks:  {len(chunks)}")

if __name__ == "__main__":
    main()