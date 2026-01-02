"""Test RAG search functionality"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import httpx
from supabase import create_client

load_dotenv(Path(__file__).parent.parent.parent / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
EMBED_MODEL = "togethercomputer/m2-bert-80M-32k-retrieval"

async def embed(text: str) -> list:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.together.xyz/v1/embeddings",
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
            json={"model": EMBED_MODEL, "input": text}
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]

async def search_rag(query: str, namespace: str = "travel"):
    print(f"🔍 Searching for: '{query}' in namespace '{namespace}'")
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    query_embedding = await embed(query)
    
    result = supabase.rpc(
        "search_rag",
        {
            "query_embedding": query_embedding,
            "target_namespace": namespace,
            "match_count": 3
        }
    ).execute()
    
    if result.data:
        print(f"\n✅ Found {len(result.data)} results:\n")
        for i, doc in enumerate(result.data, 1):
            print(f"{i}. {doc['title']} (similarity: {doc['similarity']:.3f})")
            print(f"   Preview: {doc['content'][:150]}...\n")
    else:
        print("❌ No results found")

if __name__ == "__main__":
    # Test queries
    asyncio.run(search_rag("business class flights to Paris"))
    print("-" * 50)
    asyncio.run(search_rag("hotel booking in Amsterdam"))
    print("-" * 50)
    asyncio.run(search_rag("airbnb apartment with 2 bedrooms"))
