-- Migration to update crawl_status to 'failed_verification' for domains that don't qualify
-- This updates domains where either is_law_firm or is_personal_injury_firm is false

UPDATE domains d
SET crawl_status = 'failed_verification',
    updated_at = NOW()
WHERE EXISTS (
    SELECT 1
    FROM domain_extractions de
    WHERE de.domain = d.domain
    AND de.extraction_name = 'law_firm_confirmation'
    AND (de.extraction_data->>'is_law_firm' = 'false'
         OR de.extraction_data->>'is_personal_injury_firm' = 'false')
)
AND (d.crawl_status IS NULL
     OR d.crawl_status NOT IN ('verified', 'failed_verification'));