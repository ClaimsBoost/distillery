-- Migration to update crawl_status to 'verified' for qualified personal injury law firms
-- This updates domains that have been confirmed as both law firms AND personal injury firms

UPDATE domains d
SET crawl_status = 'verified',
    updated_at = NOW()
WHERE EXISTS (
    SELECT 1
    FROM domain_extractions de
    WHERE de.domain = d.domain
    AND de.extraction_name = 'law_firm_confirmation'
    AND de.extraction_data->>'is_law_firm' = 'true'
    AND de.extraction_data->>'is_personal_injury_firm' = 'true'
)
AND (d.crawl_status IS NULL OR d.crawl_status != 'verified');

-- Report how many domains were updated
DO $$
DECLARE
    updated_count INTEGER;
BEGIN
    GET DIAGNOSTICS updated_count = ROW_COUNT;
    RAISE NOTICE 'Updated % domains to verified status', updated_count;
END $$;