import os
import httpx
from typing import List, Dict, Optional
from supabase import create_client, Client

class RAGService:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.together_api_key = os.getenv("TOGETHER_API_KEY")
        self.embed_model = "togethercomputer/m2-bert-80M-32k-retrieval"
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        if not self.together_api_key:
            raise ValueError("TOGETHER_API_KEY must be set in environment variables")
            
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

    async def embed(self, text: str) -> List[float]:
        """Generate embedding using TogetherAI"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.together.xyz/v1/embeddings",
                headers={"Authorization": f"Bearer {self.together_api_key}"},
                json={"model": self.embed_model, "input": text}
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]

    async def search(self, query: str, namespace: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant documents in a namespace"""
        try:
            query_embedding = await self.embed(query)
            
            result = self.supabase.rpc(
                "search_rag",
                {
                    "query_embedding": query_embedding,
                    "target_namespace": namespace,
                    "match_count": top_k
                }
            ).execute()
            
            return result.data
        except Exception as e:
            print(f"RAG Search Error: {e}")
            return []

    async def ingest(self, namespace: str, doc_type: str, title: str, content: str, metadata: Optional[Dict] = None):
        """Ingest a document into RAG"""
        try:
            embedding = await self.embed(content)
            
            data = {
                "namespace": namespace,
                "doc_type": doc_type,
                "title": title,
                "content": content,
                "embedding": embedding,
                "metadata": metadata or {}
            }
            
            self.supabase.table("rag_documents").insert(data).execute()
            print(f"✅ Ingested: {title}")
        except Exception as e:
            print(f"❌ Failed to ingest {title}: {e}")
            raise e
