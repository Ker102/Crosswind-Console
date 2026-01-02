"""Quick test to verify Supabase connection"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check environment variables
print("Checking environment variables...")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
together_key = os.getenv("TOGETHER_API_KEY")

if not supabase_url or "YOUR-PROJECT" in supabase_url:
    print("❌ SUPABASE_URL not set properly")
    exit(1)
else:
    print(f"✅ SUPABASE_URL: {supabase_url[:40]}...")

if not supabase_key or "your-" in supabase_key:
    print("❌ SUPABASE_KEY not set properly")
    exit(1)
else:
    print(f"✅ SUPABASE_KEY: {supabase_key[:20]}...")

if not together_key or "your-" in together_key:
    print("❌ TOGETHER_API_KEY not set properly")
    exit(1)
else:
    print(f"✅ TOGETHER_API_KEY: {together_key[:20]}...")

# Test Supabase connection
print("\nTesting Supabase connection...")
try:
    from supabase import create_client
    client = create_client(supabase_url, supabase_key)
    result = client.table("rag_documents").select("*").limit(1).execute()
    print(f"✅ Supabase connected! Table has {len(result.data)} rows")
except Exception as e:
    print(f"❌ Supabase error: {e}")
    print("\n💡 Did you run the SQL setup script in Supabase SQL Editor?")
    exit(1)

print("\n🎉 All checks passed! Ready for RAG ingestion.")
