-- Complete Supabase Database Setup for Law Firm RAG System
-- Local: nomic-embed-text (768 dimensions)
-- Production: BGE-large-en-v1.5 (1024 dimensions)

-- ============================================
-- 1. Enable Required Extensions
-- ============================================
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm; -- For text search optimization
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- For UUID generation

-- ============================================
-- 2. Note: No table drops in production
-- ============================================
-- Tables use IF NOT EXISTS to be safe in production environment

-- ============================================
-- 3. Create Main Document Vectors Table (Production)
-- ============================================
-- Production uses BGE-large-en-v1.5 (1024 dimensions)
CREATE TABLE IF NOT EXISTS document_vectors (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  document_id TEXT NOT NULL,
  content TEXT NOT NULL,
  embedding vector(1024),  -- BGE-large-en-v1.5 uses 1024 dimensions
  metadata JSONB DEFAULT '{}',
  
  -- Domain-aware fields
  domain TEXT,
  domain_id VARCHAR(12),
  
  -- Model tracking
  embedding_model TEXT DEFAULT 'BAAI/bge-large-en-v1.5',
  embedding_dimension INTEGER DEFAULT 1024,
  
  -- Tracking fields
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  CONSTRAINT document_vectors_document_id_check CHECK (document_id <> '')
);


-- ============================================
-- 4. Create Indexes for Document Vectors Table
-- ============================================

-- Production table indexes
CREATE INDEX IF NOT EXISTS idx_document_vectors_embedding 
ON document_vectors USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_document_vectors_domain 
ON document_vectors(domain);

CREATE INDEX IF NOT EXISTS idx_document_vectors_domain_id 
ON document_vectors(domain_id);

CREATE INDEX IF NOT EXISTS idx_document_vectors_document_id 
ON document_vectors(document_id);

CREATE INDEX IF NOT EXISTS idx_document_vectors_composite 
ON document_vectors(domain_id, document_id);

CREATE INDEX IF NOT EXISTS idx_document_vectors_metadata 
ON document_vectors USING gin(metadata);

CREATE INDEX IF NOT EXISTS idx_document_vectors_created_at 
ON document_vectors(created_at);

-- ============================================
-- 5. Create Vector Matching Functions
-- ============================================

-- Production match function (BGE-large-en-v1.5 - 1024 dimensions)
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(1024),
  match_count int DEFAULT 5,
  filter jsonb DEFAULT '{}'::jsonb
) RETURNS TABLE(
  id uuid,
  document_id text,
  content text,
  metadata jsonb,
  similarity float
) LANGUAGE plpgsql AS $$
BEGIN
  RETURN QUERY
  SELECT 
    dv.id,
    dv.document_id,
    dv.content,
    dv.metadata,
    1 - (dv.embedding <=> query_embedding) AS similarity
  FROM document_vectors dv
  WHERE 
    -- Apply JSON filter conditions
    CASE 
      WHEN filter ? 'document_id' THEN 
        dv.document_id = filter->>'document_id'
      WHEN filter ? '$and' THEN
        -- Handle composite filters for domain + document
        (filter->'$and'->0->>'domain_id' IS NULL OR dv.domain_id = filter->'$and'->0->>'domain_id')
        AND
        (filter->'$and'->1->>'document_id' IS NULL OR dv.document_id = filter->'$and'->1->>'document_id')
      WHEN filter ? 'domain' THEN
        dv.domain = filter->>'domain'
      WHEN filter ? 'domain_id' THEN
        dv.domain_id = filter->>'domain_id'
      ELSE TRUE
    END
  ORDER BY dv.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;


-- ============================================
-- 6. Create Domain Statistics
-- ============================================
CREATE TABLE IF NOT EXISTS domain_statistics (
  domain TEXT PRIMARY KEY,
  domain_id VARCHAR(12),
  document_count INTEGER DEFAULT 0,
  chunk_count INTEGER DEFAULT 0,
  total_size_bytes BIGINT DEFAULT 0,
  embedding_model TEXT,
  embedding_dimension INTEGER,
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);



-- ============================================
-- 7. Create Triggers
-- ============================================

create trigger handle_updated_at BEFORE
update on document_vectors for EACH row
execute FUNCTION extensions.moddatetime ('updated_at');

-- Domain statistics trigger
CREATE OR REPLACE FUNCTION update_domain_stats_on_insert()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO domain_statistics (
    domain, 
    domain_id, 
    chunk_count, 
    total_size_bytes,
    embedding_model,
    embedding_dimension
  )
  VALUES (
    NEW.domain, 
    NEW.domain_id, 
    1, 
    octet_length(NEW.content),
    NEW.embedding_model,
    NEW.embedding_dimension
  )
  ON CONFLICT (domain) DO UPDATE
  SET 
    chunk_count = domain_statistics.chunk_count + 1,
    total_size_bytes = domain_statistics.total_size_bytes + octet_length(NEW.content),
    last_updated = NOW();
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER domain_stats_insert_trigger
AFTER INSERT ON document_vectors
FOR EACH ROW
WHEN (NEW.domain IS NOT NULL)
EXECUTE FUNCTION update_domain_stats_on_insert();


-- ============================================
-- 8. Verification Queries
-- ============================================

-- Run these queries to verify setup:

-- Check setup completion
SELECT 
  'Setup complete!' as status,
  (SELECT COUNT(*) FROM pg_extension WHERE extname = 'vector') as vector_extension,
  (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'document_vectors') as tables_created;

-- Check tables were created
SELECT 
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN (
    'document_vectors',
    'domain_statistics'
  )
ORDER BY tablename;

-- ============================================
-- 9. Notes and Instructions
-- ============================================
-- 1. Run this script in your Supabase SQL editor
-- 2. Create storage buckets via Supabase Dashboard:
--    - law-firm-markdown (for production)
--    - test-markdown (for testing)
-- 3. Set environment variables:
--    - SUPABASE_URL
--    - SUPABASE_KEY
-- 4. Download embedding models for Ollama:
--    Local: ollama pull nomic-embed-text
--    Production: ollama pull bge-large
-- 5. The system automatically uses:
--    - nomic-embed-text (768 dims) for local/test
--    - BGE-large-en-v1.5 (1024 dims) for production