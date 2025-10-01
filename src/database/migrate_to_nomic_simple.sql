-- Simple migration script to change document_vectors from BGE-large-en-v1.5 (1024) to nomic-embed-text (768)
-- Use this if the table is empty or you don't need to preserve data

-- ============================================
-- 1. Drop the existing table and function
-- ============================================
DROP TABLE IF EXISTS document_vectors CASCADE;
DROP FUNCTION IF EXISTS match_documents CASCADE;

-- ============================================
-- 2. Recreate table with 768 dimensions
-- ============================================
CREATE TABLE document_vectors (
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
-- 3. Create indexes
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
-- 4. Create the match function with 768 dimensions
-- ============================================
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
-- 5. Recreate trigger
-- ============================================
CREATE TRIGGER handle_updated_at BEFORE
UPDATE ON document_vectors FOR EACH ROW
EXECUTE FUNCTION extensions.moddatetime ('updated_at');

-- Domain statistics trigger
CREATE TRIGGER domain_stats_insert_trigger
AFTER INSERT ON document_vectors
FOR EACH ROW
WHEN (NEW.domain IS NOT NULL)
EXECUTE FUNCTION update_domain_stats_on_insert();

-- ============================================
-- 6. Update domain statistics if exists
-- ============================================
UPDATE domain_statistics
SET
    embedding_model = 'nomic-embed-text',
    embedding_dimension = 768,
    last_updated = NOW()
WHERE embedding_model != 'nomic-embed-text';

-- ============================================
-- 7. Verification
-- ============================================
SELECT
    'Migration complete!' as status,
    'Table recreated with 768 dimensions' as message;

-- Check table structure
SELECT
    column_name,
    data_type,
    column_default
FROM information_schema.columns
WHERE table_name = 'document_vectors'
AND column_name IN ('embedding_model', 'embedding_dimension');

-- Check function
SELECT
    proname as function_name,
    pg_get_function_arguments(oid) as arguments
FROM pg_proc
WHERE proname = 'match_documents';