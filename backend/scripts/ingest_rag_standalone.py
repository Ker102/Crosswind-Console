"""Standalone RAG ingestion script - no app dependencies"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import httpx
from supabase import create_client

# Load env vars from project root
load_dotenv(Path(__file__).parent.parent.parent / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
EMBED_MODEL = "togethercomputer/m2-bert-80M-32k-retrieval"

async def embed(text: str) -> list:
    """Generate embedding using TogetherAI"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.together.xyz/v1/embeddings",
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
            json={"model": EMBED_MODEL, "input": text}
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]

async def ingest_all():
    print("🚀 Starting RAG ingestion...")
    
    # Connect to Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # RAG directory relative to backend folder
    rag_dir = Path(__file__).parent.parent / "data" / "rag"
    
    if not rag_dir.exists():
        print(f"❌ RAG directory not found at {rag_dir}")
        return
    
    total_files = 0
    
    # Only process direct subdirectories (namespaces like travel, jobs, trends)
    for namespace_dir in rag_dir.iterdir():
        if namespace_dir.is_dir() and not namespace_dir.name.startswith("scraped"):
            namespace = namespace_dir.name
            print(f"\n📂 Processing namespace: {namespace}")
            
            for doc_file in namespace_dir.glob("*.md"):
                doc_type = doc_file.stem
                content = doc_file.read_text(encoding='utf-8')
                
                print(f"  - Embedding {doc_file.name}...", end=" ")
                
                try:
                    embedding = await embed(content)
                    
                    data = {
                        "namespace": namespace,
                        "doc_type": doc_type,
                        "title": doc_file.name,
                        "content": content,
                        "embedding": embedding,
                        "metadata": {}
                    }
                    
                    supabase.table("rag_documents").insert(data).execute()
                    print("✅")
                    total_files += 1
                    
                except Exception as e:
                    print(f"❌ Error: {e}")
    
    print(f"\n✨ Ingestion completed! Processed {total_files} files.")

if __name__ == "__main__":
    asyncio.run(ingest_all())
