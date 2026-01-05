"""Check what's in the RAG database - titles only"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from supabase import create_client

sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

result = sb.table("rag_documents").select("namespace, title, doc_type").execute()

print(f"Total documents in RAG: {len(result.data)}")
print()

by_namespace = {}
for doc in result.data:
    ns = doc['namespace']
    if ns not in by_namespace:
        by_namespace[ns] = []
    by_namespace[ns].append(doc['title'])

for ns, titles in by_namespace.items():
    print(f"[{ns}] ({len(titles)} docs)")
    for title in titles:
        print(f"  - {title}")
    print()
