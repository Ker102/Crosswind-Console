"""Standalone Sandbox LLM test - bypasses app import chain"""
import asyncio
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

# Load env
load_dotenv(Path(__file__).parent.parent.parent / ".env")

# Direct imports (no app chain)
import httpx
from supabase import create_client

try:
    import google.generativeai as genai
except ImportError:
    genai = None
    print("Warning: google-generativeai not installed")

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@dataclass
class SandboxResult:
    text: str
    latency_ms: float
    model: str
    tools_used: List[str]
    rag_context: List[Dict]


class StandaloneRAGService:
    """Standalone RAG service for testing"""
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.together_api_key = os.getenv("TOGETHER_API_KEY")
        self.embed_model = "togethercomputer/m2-bert-80M-32k-retrieval"
        self.supabase = create_client(self.supabase_url, self.supabase_key)
    
    async def embed(self, text: str) -> List[float]:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.together.xyz/v1/embeddings",
                headers={"Authorization": f"Bearer {self.together_api_key}"},
                json={"model": self.embed_model, "input": text}
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
    
    async def search(self, query: str, namespace: str, top_k: int = 3) -> List[Dict]:
        try:
            embedding = await self.embed(query)
            result = self.supabase.rpc(
                "search_rag",
                {"query_embedding": embedding, "target_namespace": namespace, "match_count": top_k}
            ).execute()
            return result.data
        except Exception as e:
            print(f"RAG error: {e}")
            return []


# Remote MCP config
REMOTE_MCP_SERVERS = {
    "google-maps": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-google-maps"],
        "env": {"GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY", "")},
        "category": "travel"
    }
}


async def get_mcp_tools(server_name: str) -> List[Dict]:
    """Fetch tools from MCP server"""
    config = REMOTE_MCP_SERVERS.get(server_name)
    if not config:
        return []
    
    env = {**os.environ}
    if "env" in config:
        env.update(config["env"])
    
    server_params = StdioServerParameters(
        command=config["command"],
        args=config["args"],
        env=env
    )
    
    tools = []
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.list_tools()
                for tool in result.tools:
                    tools.append({
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.inputSchema,
                        "server": server_name
                    })
    except Exception as e:
        print(f"MCP error: {e}")
    
    return tools


async def test_sandbox():
    print("=" * 60)
    print("Standalone Sandbox Test")
    print("=" * 60)
    
    # Test 1: RAG
    print("\n📚 Testing RAG...")
    rag = StandaloneRAGService()
    docs = await rag.search("flight cabin class", "travel")
    print(f"   Found {len(docs)} documents")
    for doc in docs[:2]:
        print(f"   - {doc['title']}: {doc['content'][:80]}...")
    
    # Test 2: MCP Tools
    print("\n🔧 Testing MCP Tools...")
    tools = await get_mcp_tools("google-maps")
    print(f"   Found {len(tools)} tools")
    for tool in tools[:5]:
        print(f"   - {tool['name']}")
    
    # Test 3: Gemini (if available)
    if genai and os.getenv("GEMINI_API_KEY"):
        print("\n🤖 Testing Gemini...")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Build context from RAG
        rag_text = "\n".join([f"- {d['title']}: {d['content'][:200]}" for d in docs])
        
        prompt = f"""Based on this context:
{rag_text}

Question: What are the valid cabin classes for flight search?"""
        
        response = model.generate_content(prompt)
        print(f"   Response: {response.text[:300]}...")
    else:
        print("\n⚠️ Skipping Gemini test (not configured)")
    
    print("\n" + "=" * 60)
    print("✅ Standalone Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_sandbox())
