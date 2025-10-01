-- Migration script to convert existing Supabase production table from BGE-large-en-v1.5 (1024) to nomic-embed-text (768)
-- IMPORTANT: This will require re-embedding all documents since dimension size is changing

-- ============================================
-- 1. Create backup of existing data (without embeddings)
-- ============================================
CREATE TABLE IF NOT EXISTS document_vectors_backup AS
SELECT
    id,
    document_id,
    content,
    metadata,
    domain,
    domain_id,
    embedding_model,
    embedding_dimension,
    created_at,
    updated_at
FROM document_vectors;

-- ============================================
-- 2. Drop existing indexes and constraints
-- ============================================
DROP INDEX IF EXISTS idx_document_vectors_embedding;
DROP INDEX IF EXISTS idx_document_vectors_domain;
DROP INDEX IF EXISTS idx_document_vectors_domain_id;
DROP INDEX IF EXISTS idx_document_vectors_document_id;
DROP INDEX IF EXISTS idx_document_vectors_composite;
DROP INDEX IF EXISTS idx_document_vectors_metadata;
DROP INDEX IF EXISTS idx_document_vectors_created_at;

-- ============================================
-- 3. Create new table with 768 dimensions
-- ============================================
CREATE TABLE document_vectors_new (
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

    CONSTRAINT document_vectors_new_document_id_check CHECK (document_id <> '')
);

-- ============================================
-- 4. Copy data WITHOUT embeddings (they need re-generation)
-- ============================================
INSERT INTO document_vectors_new (
    id,
    document_id,
    content,
    metadata,
    domain,
    domain_id,
    embedding_model,
    embedding_dimension,
    created_at,
    updated_at
)
SELECT
    id,
    document_id,
    content,
    metadata,
    domain,
    domain_id,
    'nomic-embed-text',  -- Update model name
    768,                 -- Update dimension
    created_at,
    updated_at
FROM document_vectors;

-- ============================================
-- 5. Drop old table and rename new one
-- ============================================
DROP TABLE document_vectors;
ALTER TABLE document_vectors_new RENAME TO document_vectors;

-- ============================================
-- 6. Recreate indexes
-- ============================================
CREATE INDEX idx_document_vectors_embedding
ON document_vectors USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX idx_document_vectors_domain
ON document_vectors(domain);

CREATE INDEX idx_document_vectors_domain_id
ON document_vectors(domain_id);

CREATE INDEX idx_document_vectors_document_id
ON document_vectors(document_id);

CREATE INDEX idx_document_vectors_composite
ON document_vectors(domain_id, document_id);

CREATE INDEX idx_document_vectors_metadata
ON document_vectors USING gin(metadata);

CREATE INDEX idx_document_vectors_created_at
ON document_vectors(created_at);

-- ============================================
-- 7. Drop and recreate the match function with 768 dimensions
-- ============================================
DROP FUNCTION IF EXISTS match_documents(vector(1024), int, jsonb);

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

-- ============================================
-- 8. Recreate trigger
-- ============================================
CREATE TRIGGER handle_updated_at BEFORE
UPDATE ON document_vectors FOR EACH ROW
EXECUTE FUNCTION extensions.moddatetime ('updated_at');

-- Recreate domain statistics trigger
CREATE TRIGGER domain_stats_insert_trigger
AFTER INSERT ON document_vectors
FOR EACH ROW
WHEN (NEW.domain IS NOT NULL)
EXECUTE FUNCTION update_domain_stats_on_insert();

-- ============================================
-- 9. Update domain statistics table
-- ============================================
UPDATE domain_statistics
SET
    embedding_model = 'nomic-embed-text',
    embedding_dimension = 768,
    last_updated = NOW();

-- ============================================
-- 10. Verification
-- ============================================
SELECT
    'Migration complete!' as status,
    COUNT(*) as total_records,
    COUNT(embedding) as records_with_embeddings
FROM document_vectors;

-- Check that function was recreated correctly
SELECT
    proname as function_name,
    pg_get_function_arguments(oid) as arguments
FROM pg_proc
WHERE proname = 'match_documents';

-- ============================================
-- IMPORTANT NOTES:
-- ============================================
-- 1. After running this migration, you MUST re-embed all documents
--    using the nomic-embed-text model (768 dimensions)
-- 2. The backup table (document_vectors_backup) is kept for safety
--    You can drop it after verifying the migration:
--    DROP TABLE document_vectors_backup;
-- 3. Run the embedding command to regenerate embeddings:
--    python -m src.cli embed --force