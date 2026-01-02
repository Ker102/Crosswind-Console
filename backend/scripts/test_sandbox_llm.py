"""Test the Sandbox LLM endpoint"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load env
load_dotenv(Path(__file__).parent.parent.parent / ".env")

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.sandbox_llm import SandboxLLMService

async def test_sandbox():
    print("=" * 60)
    print("Testing Sandbox LLM Service (RAG + Remote MCP)")
    print("=" * 60)
    
    service = SandboxLLMService(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        model_id="gemini-2.0-flash"
    )
    
    # Test 1: Simple query that should use RAG
    print("\n📝 Test 1: Query with RAG context")
    print("-" * 40)
    
    result = await service.respond_sandbox(
        prompt="What cabin classes are available for flights?",
        namespace="travel"
    )
    
    print(f"✅ Response: {result.text[:300]}...")
    print(f"📊 Latency: {result.latency_ms:.0f}ms")
    print(f"🔧 Tools used: {result.tools_used}")
    print(f"📚 RAG docs: {[d['title'] for d in result.rag_context]}")
    
    # Test 2: Query that should trigger tool calls
    print("\n\n📝 Test 2: Query requiring tool calls")
    print("-" * 40)
    
    result = await service.respond_sandbox(
        prompt="Search for hotels near the Eiffel Tower in Paris",
        namespace="travel"
    )
    
    print(f"✅ Response: {result.text[:500]}...")
    print(f"📊 Latency: {result.latency_ms:.0f}ms")
    print(f"🔧 Tools used: {result.tools_used}")
    print(f"📚 RAG docs: {[d['title'] for d in result.rag_context]}")
    
    print("\n" + "=" * 60)
    print("Sandbox LLM Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_sandbox())
