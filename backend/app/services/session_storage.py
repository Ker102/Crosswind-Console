"""
Session Storage Service - Supabase-based persistence for Trip Planner sessions.
Stores and retrieves TripState between graph executions.
"""
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass

from supabase import create_client, Client

from ..config import get_settings


@dataclass
class TripSession:
    """Represents a stored trip planning session."""
    session_id: str
    user_id: Optional[str]
    state: Dict[str, Any]
    phase: str
    created_at: datetime
    updated_at: datetime
    is_complete: bool


class SessionStorageService:
    """
    Handles persistence of Trip Planner sessions to Supabase.
    
    Table schema (trip_sessions):
    - id: uuid (primary key)
    - user_id: text (optional, for multi-user support)
    - state: jsonb (the full TripState)
    - phase: text (current workflow phase)
    - is_complete: boolean
    - created_at: timestamptz
    - updated_at: timestamptz
    """
    
    TABLE_NAME = "trip_sessions"
    
    def __init__(self):
        settings = get_settings()
        if not settings.supabase_url or not settings.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
        
        self._client: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
    
    async def create_session(
        self,
        state: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> str:
        """
        Create a new trip planning session.
        
        Returns:
            session_id: UUID of the created session
        """
        result = self._client.table(self.TABLE_NAME).insert({
            "user_id": user_id,
            "state": state,
            "phase": state.get("phase", "parsing"),
            "is_complete": False
        }).execute()
        
        return result.data[0]["id"]
    
    async def get_session(self, session_id: str) -> Optional[TripSession]:
        """
        Retrieve a session by ID.
        
        Returns:
            TripSession if found, None otherwise
        """
        result = self._client.table(self.TABLE_NAME).select("*").eq(
            "id", session_id
        ).execute()
        
        if not result.data:
            return None
        
        row = result.data[0]
        return TripSession(
            session_id=row["id"],
            user_id=row.get("user_id"),
            state=row["state"],
            phase=row["phase"],
            created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(row["updated_at"].replace("Z", "+00:00")),
            is_complete=row["is_complete"]
        )
    
    async def update_session(
        self,
        session_id: str,
        state: Dict[str, Any],
        is_complete: bool = False
    ) -> bool:
        """
        Update an existing session with new state.
        
        Returns:
            True if update succeeded
        """
        result = self._client.table(self.TABLE_NAME).update({
            "state": state,
            "phase": state.get("phase", "unknown"),
            "is_complete": is_complete,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", session_id).execute()
        
        return len(result.data) > 0
    
    async def list_user_sessions(
        self,
        user_id: str,
        limit: int = 10,
        include_complete: bool = False
    ) -> List[TripSession]:
        """
        List sessions for a specific user.
        
        Args:
            user_id: User identifier
            limit: Max sessions to return
            include_complete: Whether to include completed sessions
        
        Returns:
            List of TripSession objects
        """
        query = self._client.table(self.TABLE_NAME).select("*").eq(
            "user_id", user_id
        ).order("updated_at", desc=True).limit(limit)
        
        if not include_complete:
            query = query.eq("is_complete", False)
        
        result = query.execute()
        
        return [
            TripSession(
                session_id=row["id"],
                user_id=row.get("user_id"),
                state=row["state"],
                phase=row["phase"],
                created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00")),
                updated_at=datetime.fromisoformat(row["updated_at"].replace("Z", "+00:00")),
                is_complete=row["is_complete"]
            )
            for row in result.data
        ]
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session by ID."""
        result = self._client.table(self.TABLE_NAME).delete().eq(
            "id", session_id
        ).execute()
        return len(result.data) > 0


# Singleton instance
_session_storage: Optional[SessionStorageService] = None

def get_session_storage() -> SessionStorageService:
    """Get singleton session storage instance."""
    global _session_storage
    if _session_storage is None:
        _session_storage = SessionStorageService()
    return _session_storage
