"""
Test script for Session Storage with Supabase.
"""
import asyncio
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent.parent / ".env")


async def test_session_storage():
    print("=" * 60)
    print("Testing Session Storage (Supabase)")
    print("=" * 60)
    
    from app.services.session_storage import get_session_storage
    
    storage = get_session_storage()
    
    # Test 1: Create a session
    print("\n1. Creating test session...")
    test_state = {
        "origin": "LHR",
        "destination": "CDG",
        "start_date": "2026-04-20",
        "end_date": "2026-04-25",
        "travelers": 2,
        "phase": "testing",
        "flights": [],
        "hotels": [],
        "messages": ["Test session created"]
    }
    
    session_id = await storage.create_session(test_state, user_id="test_user_123")
    print(f"   [OK] Created session: {session_id}")
    
    # Test 2: Retrieve the session
    print("\n2. Retrieving session...")
    session = await storage.get_session(session_id)
    if session:
        print(f"   [OK] Retrieved session:")
        print(f"      - ID: {session.session_id}")
        print(f"      - User: {session.user_id}")
        print(f"      - Phase: {session.phase}")
        print(f"      - Origin: {session.state.get('origin')}")
        print(f"      - Destination: {session.state.get('destination')}")
    else:
        print("   [FAIL] Failed to retrieve session")
    
    # Test 3: List user sessions
    print("\n3. Listing user sessions...")
    sessions = await storage.list_user_sessions("test_user_123", limit=5)
    print(f"   [OK] Found {len(sessions)} session(s) for test_user_123")
    
    # Test 4: Update session
    print("\n4. Updating session...")
    test_state["phase"] = "complete"
    test_state["messages"].append("Session completed")
    success = await storage.update_session(session_id, test_state, is_complete=True)
    print(f"   [{'OK' if success else 'FAIL'}] Update {'succeeded' if success else 'failed'}")
    
    # Test 5: Delete session (cleanup)
    print("\n5. Deleting test session...")
    deleted = await storage.delete_session(session_id)
    print(f"   [{'OK' if deleted else 'FAIL'}] Delete {'succeeded' if deleted else 'failed'}")
    
    print("\n" + "=" * 60)
    print("[OK] Session Storage Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_session_storage())
