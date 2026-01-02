import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to allow importing app modules
import sys
sys.path.append(str(Path(__file__).parent.parent))

from app.services.rag_service import RAGService

# Load env vars
load_dotenv()

async def ingest_all():
    try:
        print("🚀 Starting RAG ingestion...")
        
        rag = RAGService()
        rag_dir = Path("data/rag")
        
        if not rag_dir.exists():
            print(f"❌ RAG directory not found at {rag_dir}")
            return

        total_files = 0
        
        # Iterate through namespaces (travel, jobs, trends)
        for namespace_dir in rag_dir.iterdir():
            if namespace_dir.is_dir():
                namespace = namespace_dir.name
                print(f"\n📂 Processing namespace: {namespace}")
                
                for doc_file in namespace_dir.glob("*.md"):
                    # Use filename stem as doc_type (e.g., 'flight_params.md' -> 'flight_params')
                    doc_type = doc_file.stem 
                    content = doc_file.read_text(encoding='utf-8')
                    
                    print(f"  - Ingesting {doc_file.name}...")
                    
                    await rag.ingest(
                        namespace=namespace,
                        doc_type=doc_type,
                        title=doc_file.name,
                        content=content
                    )
                    total_files += 1
        
        print(f"\n✨ Ingestion completed! Processed {total_files} files.")
        
    except Exception as e:
        print(f"\n❌ Ingestion failed: {e}")
        # Check specific errors
        if "relation \"rag_documents\" does not exist" in str(e):
            print("\n💡 Tip: Did you run the 'setup_rag.sql' script in Supabase?")
        if "SUPABASE_" in str(e):
            print("\n💡 Tip: Check your .env file for SUPABASE_URL and SUPABASE_KEY")

if __name__ == "__main__":
    asyncio.run(ingest_all())
