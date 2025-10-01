-- ============================================
-- Complete Supabase Database Setup for Law Firm RAG System
-- Uses nomic-embed-text (768 dimensions)
-- ============================================
-- Run this in your Supabase SQL Editor
--
-- Prerequisites:
-- 1. Supabase project created
-- 2. Database URL and anon key configured
--
-- ============================================

-- ============================================
-- 1. Enable Required Extensions
-- ============================================
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm; -- For text search optimization
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- For UUID generation

-- ============================================
-- 2. Create Document Vectors Table
-- ============================================
CREATE TABLE IF NOT EXISTS document_vectors (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  document_id TEXT NOT NULL,
  content TEXT NOT NULL,
  embedding vector(768),  -- nomic-embed-text uses 768 dimensions
  metadata JSONB DEFAULT '{}',

  -- Domain-aware fields
  domain TEXT,
  domain_id VARCHAR(12),

  -- Model tracking
  embedding_model TEXT DEFAULT 'nomic-embed-text',
  embedding_dimension INTEGER DEFAULT 768,

  -- Tracking fields
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  CONSTRAINT document_vectors_document_id_check CHECK (document_id <> '')
);

-- ============================================
-- 3. Create Indexes for Efficient Querying
-- ============================================
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
-- 4. Create Domain Statistics Table
-- ============================================
CREATE TABLE IF NOT EXISTS domain_statistics (
  domain TEXT PRIMARY KEY,
  domain_id VARCHAR(12),
  document_count INTEGER DEFAULT 0,
  chunk_count INTEGER DEFAULT 0,
  total_size_bytes BIGINT DEFAULT 0,
  embedding_model TEXT DEFAULT 'nomic-embed-text',
  embedding_dimension INTEGER DEFAULT 768,
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 5. Add Embedding Tracking to domain_paths (if table exists)
-- ============================================
-- Add embedding tracking columns if domain_paths table exists
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'domain_paths') THEN
    -- Add is_embedded column
    ALTER TABLE domain_paths
    ADD COLUMN IF NOT EXISTS is_embedded BOOLEAN DEFAULT false;

    -- Add last_embedded_at column
    ALTER TABLE domain_paths
    ADD COLUMN IF NOT EXISTS last_embedded_at TIMESTAMP WITH TIME ZONE;

    -- Create indexes for efficient queries
    CREATE INDEX IF NOT EXISTS idx_domain_paths_is_embedded
    ON domain_paths(is_embedded);

    CREATE INDEX IF NOT EXISTS idx_domain_paths_last_embedded_at
    ON domain_paths(last_embedded_at);

    CREATE INDEX IF NOT EXISTS idx_domain_paths_domain_embedded
    ON domain_paths(domain, is_embedded);
  END IF;
END $$;

-- ============================================
-- 6. Create Core Functions
-- ============================================

-- Vector matching function
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(768),
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

-- Domain statistics update function
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

-- ============================================
-- 7. Embedding Tracking Functions
-- ============================================

-- Mark a single path as embedded
CREATE OR REPLACE FUNCTION mark_path_as_embedded(
    p_domain TEXT,
    p_path_slug TEXT
) RETURNS BOOLEAN AS $$
DECLARE
    v_updated BOOLEAN;
BEGIN
    UPDATE domain_paths
    SET
        is_embedded = true,
        last_embedded_at = NOW(),
        updated_at = NOW()
    WHERE domain = p_domain
        AND path_slug = p_path_slug;

    v_updated := FOUND;
    RETURN v_updated;
END;
$$ LANGUAGE plpgsql;

-- Mark multiple paths as embedded
CREATE OR REPLACE FUNCTION mark_paths_as_embedded(
    p_url_hashes TEXT[]
) RETURNS INTEGER AS $$
DECLARE
    v_count INTEGER;
BEGIN
    UPDATE domain_paths
    SET
        is_embedded = true,
        last_embedded_at = NOW(),
        updated_at = NOW()
    WHERE url_hash = ANY(p_url_hashes);

    GET DIAGNOSTICS v_count = ROW_COUNT;
    RETURN v_count;
END;
$$ LANGUAGE plpgsql;

-- Get embedding status for a domain
CREATE OR REPLACE FUNCTION get_domain_embedding_status(
    p_domain TEXT
) RETURNS TABLE(
    total_paths BIGINT,
    embedded_paths BIGINT,
    pending_paths BIGINT,
    last_embedded_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(*) AS total_paths,
        COUNT(*) FILTER (WHERE is_embedded = true) AS embedded_paths,
        COUNT(*) FILTER (WHERE is_embedded = false OR is_embedded IS NULL) AS pending_paths,
        MAX(last_embedded_at) AS last_embedded_at
    FROM domain_paths
    WHERE domain = p_domain;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 8. Create Triggers
-- ============================================

-- Update timestamp trigger using Supabase's moddatetime extension
CREATE TRIGGER handle_updated_at BEFORE UPDATE ON document_vectors
FOR EACH ROW EXECUTE FUNCTION extensions.moddatetime('updated_at');

-- Domain statistics trigger
CREATE TRIGGER domain_stats_insert_trigger
AFTER INSERT ON document_vectors
FOR EACH ROW
WHEN (NEW.domain IS NOT NULL)
EXECUTE FUNCTION update_domain_stats_on_insert();

-- ============================================
-- 9. Enable Row Level Security (Optional)
-- ============================================
-- Uncomment if you want to enable RLS
-- ALTER TABLE document_vectors ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE domain_statistics ENABLE ROW LEVEL SECURITY;

-- ============================================
-- 10. Verification
-- ============================================

-- Check setup completion
SELECT
  'Supabase setup complete!' as status,
  (SELECT COUNT(*) FROM pg_extension WHERE extname = 'vector') as vector_extension,
  (SELECT COUNT(*) FROM information_schema.tables
   WHERE table_name IN ('document_vectors', 'domain_statistics')) as tables_created,
  (SELECT COUNT(*) FROM pg_proc
   WHERE proname IN ('match_documents', 'mark_path_as_embedded', 'get_domain_embedding_status')) as functions_created;

-- Display table sizes
SELECT
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN ('document_vectors', 'domain_statistics', 'domain_paths')
ORDER BY tablename;

-- ============================================
-- Notes for Supabase:
-- ============================================
-- 1. Create storage buckets via Supabase Dashboard:
--    - law-firm-markdown (for production)
--    - law-firm-websites (for production)
-- 2. Set environment variables:
--    - SUPABASE_URL
--    - SUPABASE_KEY
-- 3. Ensure Ollama is installed locally: ollama pull nomic-embed-text
-- 4. This setup uses 768 dimensions for nomic-embed-text
-- 5. Consider enabling RLS for production use
-- ============================================