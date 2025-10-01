-- Query to combine all most recent extractions for a domain into a single JSON object
-- Usage: psql -U postgres -d claimsboost -v domain="'137law.com'" -f get_domain_extractions.sql

WITH latest_extractions AS (
    SELECT
        domain,
        extraction_name,
        extraction_data,
        extracted_at,
        ROW_NUMBER() OVER (
            PARTITION BY domain, extraction_name
            ORDER BY extracted_at DESC
        ) as rn
    FROM domain_extractions
    WHERE domain = :domain
        AND path_id IS NULL  -- Domain-level extractions only
),
combined AS (
    SELECT
        domain,
        jsonb_object_agg(
            extraction_name,
            -- Remove _api_request field from extraction data
            extraction_data - '_api_request'
        ) as extractions
    FROM latest_extractions
    WHERE rn = 1
    GROUP BY domain
)
SELECT
    jsonb_pretty(
        jsonb_build_object(
            'domain', domain,
            'extraction_timestamp', NOW(),
            'extractions', extractions
        )
    ) as combined_data
FROM combined;