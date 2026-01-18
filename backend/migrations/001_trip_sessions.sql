-- Trip Sessions Table for LangGraph Session Persistence
-- Run this in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS trip_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT,  -- Optional, for multi-user support
    state JSONB NOT NULL,  -- Full TripState as JSON
    phase TEXT NOT NULL DEFAULT 'parsing',
    is_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for user lookups
CREATE INDEX IF NOT EXISTS idx_trip_sessions_user_id ON trip_sessions(user_id);

-- Index for incomplete sessions
CREATE INDEX IF NOT EXISTS idx_trip_sessions_incomplete ON trip_sessions(is_complete) WHERE is_complete = FALSE;

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER update_trip_sessions_updated_at
    BEFORE UPDATE ON trip_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (optional, if using Supabase Auth)
-- ALTER TABLE trip_sessions ENABLE ROW LEVEL SECURITY;
