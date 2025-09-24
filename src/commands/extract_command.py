"""
Extract command handler
Handles office location extraction from embedded documents
"""

import json
import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..core.settings import get_settings, Settings
from ..extract import (
    OfficeLocationsExtractor,
    LawFirmConfirmationExtractor,
    YearFoundedExtractor,
    TotalSettlementsExtractor,
    LanguagesSpokenExtractor,
    PracticeAreasExtractor,
    AttorneysExtractor,
    SocialMediaExtractor,
    CompanyDescriptionExtractor,
    StatesServedExtractor,
    ContactInfoExtractor
)
from ..database import get_database_connection

logger = logging.getLogger(__name__)


class ExtractCommand:
    """Handles extract command operations"""
    
    def __init__(self, settings: Settings = None, supabase_client=None):
        """
        Initialize extract command
        
        Args:
            settings: Application settings (uses global if not provided)
            supabase_client: Optional Supabase client
        """
        self.settings = settings or get_settings()
        self.supabase_client = supabase_client
        self.extractors = {
            'office_locations': OfficeLocationsExtractor(self.settings, supabase_client),
            'law_firm_confirmation': LawFirmConfirmationExtractor(self.settings, supabase_client),
            'year_founded': YearFoundedExtractor(self.settings, supabase_client),
            'total_settlements': TotalSettlementsExtractor(self.settings, supabase_client),
            'languages_spoken': LanguagesSpokenExtractor(self.settings, supabase_client),
            'practice_areas': PracticeAreasExtractor(self.settings, supabase_client),
            'attorneys': AttorneysExtractor(self.settings, supabase_client),
            'social_media': SocialMediaExtractor(self.settings, supabase_client),
            'company_description': CompanyDescriptionExtractor(self.settings, supabase_client),
            'states_served': StatesServedExtractor(self.settings, supabase_client),
            'contact_info': ContactInfoExtractor(self.settings, supabase_client)
        }
        # Get database connection for storing results
        self.db_conn = get_database_connection()
    
    def execute(self, targets: List[str], extraction_type: str,
                is_domain: bool = False) -> Dict[str, Any]:
        """
        Execute extraction for multiple targets

        Args:
            targets: List of document IDs or domain names
            extraction_type: Type of extraction (specific type or 'all')
            is_domain: Whether targets are domains or documents

        Returns:
            Extraction results
        """
        logger.info(f"\n{'='*60}")

        # Handle 'all' extraction type
        if extraction_type == 'all':
            logger.info(f"Running ALL extractors on {len(targets)} {'domains' if is_domain else 'documents'}")
            logger.info(f"{'='*60}")
            return self._execute_all_extractors(targets, is_domain)

        logger.info(f"Extracting {extraction_type} from {len(targets)} {'domains' if is_domain else 'documents'}")
        logger.info(f"{'='*60}")

        # Get the appropriate extractor
        if extraction_type not in self.extractors:
            available = list(self.extractors.keys()) + ['all']
            raise ValueError(f"Unknown extraction type: {extraction_type}. Supported types: {available}")

        extractor = self.extractors[extraction_type]

        all_results = []

        for target in targets:
            logger.info(f"Processing target: {target}")

            if is_domain:
                # Extract from entire domain
                logger.info(f"Performing extraction across domain {target}")
                result = extractor.extract_from_domain(target)
            else:
                # Extract from specific document
                logger.info(f"Performing extraction for document {target}")
                result = extractor.extract_from_document(target)

            all_results.append({
                'target': target,
                'type': 'domain' if is_domain else 'document',
                'data': result
            })

            # Store successful extraction in database
            if result and not result.get('error'):
                self._store_extraction(target, extraction_type, result, is_domain)
        
        # Format final results
        return {
            'extraction_type': extraction_type,
            'targets': targets,
            'target_type': 'domain' if is_domain else 'document',
            'timestamp': datetime.now().isoformat(),
            'results': all_results,
            'summary': {
                'total_targets': len(targets),
                'successful': sum(1 for r in all_results if r.get('data') and not r['data'].get('error'))
            },
            'config': {
                'model': self.settings.extraction.model_type,
                'temperature': self.settings.extraction.temperature,
                'k_chunks': self.settings.extraction.k_chunks
            }
        }
    
    def _execute_all_extractors(self, targets: List[str], is_domain: bool) -> Dict[str, Any]:
        """
        Execute all extractors for the given targets

        Args:
            targets: List of document IDs or domain names
            is_domain: Whether targets are domains or documents

        Returns:
            Combined extraction results
        """
        all_results = []
        extractor_summary = {}

        # Skip the legacy alias
        extractor_types = [k for k in self.extractors.keys() if k != 'short_description']

        for target in targets:
            logger.info(f"\n{'-'*40}")
            logger.info(f"Processing target: {target}")
            logger.info(f"{'-'*40}")

            target_results = {
                'target': target,
                'type': 'domain' if is_domain else 'document',
                'extractions': {}
            }

            for extraction_type in extractor_types:
                logger.info(f"  Running {extraction_type}...")
                extractor = self.extractors[extraction_type]

                try:
                    if is_domain:
                        result = extractor.extract_from_domain(target)
                    else:
                        result = extractor.extract_from_document(target)

                    if result and not result.get('error'):
                        target_results['extractions'][extraction_type] = result
                        self._store_extraction(target, extraction_type, result, is_domain)
                        logger.info(f"    ✓ {extraction_type} completed")

                        # Update summary
                        if extraction_type not in extractor_summary:
                            extractor_summary[extraction_type] = {'success': 0, 'failed': 0}
                        extractor_summary[extraction_type]['success'] += 1
                    else:
                        error_msg = result.get('error', 'No data extracted') if result else 'No data extracted'
                        logger.warning(f"    ✗ {extraction_type} failed: {error_msg}")
                        target_results['extractions'][extraction_type] = {'error': error_msg}

                        if extraction_type not in extractor_summary:
                            extractor_summary[extraction_type] = {'success': 0, 'failed': 0}
                        extractor_summary[extraction_type]['failed'] += 1

                except Exception as e:
                    logger.error(f"    ✗ {extraction_type} error: {str(e)}")
                    target_results['extractions'][extraction_type] = {'error': str(e)}

                    if extraction_type not in extractor_summary:
                        extractor_summary[extraction_type] = {'success': 0, 'failed': 0}
                    extractor_summary[extraction_type]['failed'] += 1

            all_results.append(target_results)

        return {
            'extraction_type': 'all',
            'targets': targets,
            'target_type': 'domain' if is_domain else 'document',
            'timestamp': datetime.now().isoformat(),
            'results': all_results,
            'summary': {
                'total_targets': len(targets),
                'extractors_run': len(extractor_types),
                'by_extractor': extractor_summary
            },
            'config': {
                'model': self.settings.extraction.model_type,
                'temperature': self.settings.extraction.temperature,
                'k_chunks': self.settings.extraction.k_chunks
            }
        }

    def save_results(self, results: Dict[str, Any], output_path: str):
        """
        Save extraction results to file
        
        Args:
            results: Extraction results
            output_path: Path to save results
        """
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {output_path}")
    
    def display_results(self, results: Dict[str, Any]):
        """
        Display extraction results
        
        Args:
            results: Results dictionary from execute()
        """
        print(json.dumps(results, indent=2))
    
    def _store_extraction(self, target: str, extraction_type: str, 
                         result: Dict[str, Any], is_domain: bool):
        """
        Store extraction result in database
        
        Args:
            target: Domain or document ID
            extraction_type: Type of extraction
            result: Extraction result data
            is_domain: Whether target is a domain
        """
        try:
            # Prepare data for storage
            # Keep _api_request but remove other internal metadata
            clean_result = {k: v for k, v in result.items()
                          if not k.startswith('_') or k == '_api_request'}

            # Generate unique ID
            extraction_id = str(uuid.uuid4())
            
            # Determine domain and path_id
            if is_domain:
                domain = target
                path_id = None  # Domain-level extraction
            else:
                # For document extractions, try to extract domain
                parts = target.split('/')
                domain = parts[0] if parts else target
                path_id = target
            
            # Insert into database
            with self.db_conn.get_postgres_connection() as (conn, cur):
                cur.execute("""
                    INSERT INTO domain_extractions 
                    (id, domain, path_id, extraction_name, extraction_version, 
                     extraction_data, extracted_at, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (
                    extraction_id,
                    domain,
                    path_id,
                    extraction_type,
                    self.settings.extraction.model_type,  # Use model as version
                    json.dumps(clean_result),
                    datetime.now(),
                    datetime.now(),
                    datetime.now()
                ))
                conn.commit()
                
                if cur.rowcount > 0:
                    logger.info(f"Stored extraction for {target} in database (ID: {extraction_id})")
                else:
                    logger.warning(f"Extraction already exists for {target}")
                    
        except Exception as e:
            logger.error(f"Failed to store extraction: {str(e)}")
            # Don't fail the whole extraction if storage fails
            pass