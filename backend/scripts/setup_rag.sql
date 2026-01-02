-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store your documents
create table if not exists rag_documents (
  id uuid primary key default gen_random_uuid(),
  namespace text not null, -- 'travel', 'jobs', 'trends'
  doc_type text not null,  -- 'tool_guidance', 'params', 'domain'
  title text not null,
  content text not null,
  embedding vector (768),  -- m2-bert-80M-32k-retrieval uses 768 dimensions
  metadata jsonb,
  created_at timestamp with time zone default now()
);

-- Create a search function that we can call from our client
create or replace function search_rag (
  query_embedding vector(768),
  target_namespace text,
  match_count int default 5
) returns table (
  id uuid,
  title text,
  content text,
  similarity float
) language plpgsql as $$
begin
  return query
  select
    rag_documents.id,
    rag_documents.title,
    rag_documents.content,
    1 - (rag_documents.embedding <=> query_embedding) as similarity
  from rag_documents
  where rag_documents.namespace = target_namespace
  order by rag_documents.embedding <=> query_embedding
  limit match_count;
end;
$$;

-- Create an index for faster queries (IVFFlat)
-- Note: This is effective once you have a bit of data. 
-- For small datasets, exact search without index is fast enough, but good to have.
create index on rag_documents using ivfflat (embedding vector_cosine_ops)
with
  (lists = 100);
