"""Ingest MCP API docs into RAG database"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

import httpx
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
EMBED_MODEL = "togethercomputer/m2-bert-80M-32k-retrieval"

sb = create_client(SUPABASE_URL, SUPABASE_KEY)


async def embed(text: str) -> list:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.together.xyz/v1/embeddings",
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
            json={"model": EMBED_MODEL, "input": text}
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]


async def ingest_doc(namespace: str, title: str, doc_type: str, content: str):
    """Ingest a single document into RAG"""
    try:
        # Check if already exists
        existing = sb.table("rag_documents").select("id").eq("namespace", namespace).eq("title", title).execute()
        if existing.data:
            print(f"⚠️  Already exists: [{namespace}] {title}")
            return False
        
        embedding = await embed(content)
        
        data = {
            "namespace": namespace,
            "doc_type": doc_type,
            "title": title,
            "content": content,
            "embedding": embedding,
            "metadata": {}
        }
        
        sb.table("rag_documents").insert(data).execute()
        print(f"✅ Ingested: [{namespace}] {title}")
        return True
    except Exception as e:
        print(f"❌ Failed: {title} - {e}")
        return False


async def main():
    print("=" * 60)
    print("Ingesting MCP API Docs into RAG")
    print("=" * 60)
    
    api_docs_dir = Path(__file__).parent.parent.parent / "mcp_servers" / "api_docs"
    travel_rag_dir = Path(__file__).parent.parent / "data" / "rag" / "travel"
    
    docs_to_ingest = [
        # MCP API docs (cleaner versions)
        (api_docs_dir / "sky_params.md", "travel", "api_reference", "Flights Sky API Reference"),
        (api_docs_dir / "kiwi_params.md", "travel", "api_reference", "Kiwi API Reference"),
        
        # Travel RAG docs (ensure all are ingested)
        (travel_rag_dir / "flight_params.md", "travel", "parameter_guide", "flight_params.md"),
        (travel_rag_dir / "hotel_params.md", "travel", "parameter_guide", "hotel_params.md"),
        (travel_rag_dir / "airbnb_params.md", "travel", "parameter_guide", "airbnb_params.md"),
        (travel_rag_dir / "google_maps_guidance.md", "travel", "parameter_guide", "google_maps_guidance.md"),
        (travel_rag_dir / "tool_guidance.md", "travel", "tool_guidance", "tool_guidance.md"),
        (travel_rag_dir / "flights_sky_config.md", "travel", "config", "flights_sky_config.md"),
    ]
    
    ingested = 0
    for path, namespace, doc_type, title in docs_to_ingest:
        if path.exists():
            content = path.read_text(encoding="utf-8")
            if await ingest_doc(namespace, title, doc_type, content):
                ingested += 1
        else:
            print(f"❌ File not found: {path}")
    
    print()
    print(f"Ingested {ingested} new documents")
    
    # Show current RAG state
    result = sb.table("rag_documents").select("namespace, title").execute()
    print(f"\nTotal documents in RAG: {len(result.data)}")
    for doc in result.data:
        print(f"  [{doc['namespace']}] {doc['title']}")


if __name__ == "__main__":
    asyncio.run(main())
