"""
Test script for LangChain Sandbox Service
"""
import asyncio
import os
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env")

async def test_sandbox():
    print("=" * 60)
    print("Testing LangChain Sandbox Service")
    print("=" * 60)
    
    # Import and create service
    from app.services.sandbox_llm import LangChainSandboxService
    
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        print("❌ GEMINI_API_KEY not set!")
        return
    
    print("\n1. Creating LangChain sandbox service...")
    service = LangChainSandboxService(
        gemini_api_key=api_key,
        model_id="gemini-2.0-flash"
    )
    
    print("\n2. Testing flight search prompt...")
    prompt = "Find flights from London to Paris on April 20, 2026"
    
    import time
    start = time.time()
    
    result = await service.process(
        prompt=prompt,
        namespace="travel"
    )
    
    elapsed = time.time() - start
    
    print(f"\n--- Result (took {elapsed:.2f}s) ---")
    print(f"Model: {result.model}")
    print(f"Latency: {result.latency_ms:.0f}ms")
    print(f"Tools Used: {result.tools_used}")
    print(f"RAG Context: {len(result.rag_context)} docs")
    print(f"\nResponse:\n{result.text[:500]}...")
    
    print("\n✅ LangChain Sandbox test complete!")

if __name__ == "__main__":
    asyncio.run(test_sandbox())
