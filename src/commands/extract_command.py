"""
Extract command handler
Handles office location extraction from embedded documents
"""

import json
import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

from ..core.settings import get_settings, Settings
from ..extract import (
    OfficeLocationsExtractor,
    LawFirmConfirmationExtractor,
    YearFoundedExtractor,
    TotalSettlementsExtractor,
    SupportedLanguagesExtractor,
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
            'supported_languages': SupportedLanguagesExtractor(self.settings, supabase_client),
            'practice_areas': PracticeAreasExtractor(self.settings, supabase_client),
            'attorneys': AttorneysExtractor(self.settings, supabase_client),
            'social_media': SocialMediaExtractor(self.settings, supabase_client),
            'company_description': CompanyDescriptionExtractor(self.settings, supabase_client),
            'states_served': StatesServedExtractor(self.settings, supabase_client),
            'contact_info': ContactInfoExtractor(self.settings, supabase_client)
        }
        # Get database connection for storing results
        self.db_conn = get_database_connection()

        # Thread safety for parallel processing
        self.db_lock = threading.Lock()
        self.progress_lock = threading.Lock()
        self.completed_count = 0
    
    def execute(self, targets: List[str], extraction_type: str,
                is_domain: bool = False, force: bool = False, workers: int = 1) -> Dict[str, Any]:
        """
        Execute extraction for multiple targets

        Args:
            targets: List of document IDs or domain names
            extraction_type: Type of extraction (specific type or 'all')
            is_domain: Whether targets are domains or documents
            force: Force extraction even if data already exists
            workers: Number of parallel workers

        Returns:
            Extraction results
        """
        logger.info(f"\n{'='*60}")

        # Handle 'all' extraction type
        if extraction_type == 'all':
            logger.info(f"Running ALL extractors on {len(targets)} {'domains' if is_domain else 'documents'}")
            if force:
                logger.info("Force mode enabled - will overwrite existing extractions")
            logger.info(f"{'='*60}")
            return self._execute_all_extractors(targets, is_domain, force)

        logger.info(f"Extracting {extraction_type} from {len(targets)} {'domains' if is_domain else 'documents'}")
        if workers > 1:
            logger.info(f"Using {workers} parallel workers")
        logger.info(f"{'='*60}")

        # Get the appropriate extractor
        if extraction_type not in self.extractors:
            available = list(self.extractors.keys()) + ['all']
            raise ValueError(f"Unknown extraction type: {extraction_type}. Supported types: {available}")

        extractor = self.extractors[extraction_type]

        # Use parallel processing if workers > 1
        if workers > 1:
            return self._execute_parallel(
                targets, extraction_type, extractor, is_domain, force, workers
            )

        # Otherwise use sequential processing (existing code)
        all_results = []

        for i, target in enumerate(targets, 1):
            logger.info(f"[{i}/{len(targets)}] Processing target: {target}")

            # Check if extraction already exists (unless forced)
            if not force and is_domain and self._extraction_exists(target, extraction_type):
                logger.info(f"Skipping {target} - {extraction_type} extraction already exists")
                print(f"[{i}/{len(targets)}] Skipping {target} (already extracted)...")
                all_results.append({
                    'target': target,
                    'type': 'domain',
                    'data': {'skipped': True, 'reason': 'Already extracted'}
                })
                continue

            print(f"[{i}/{len(targets)}] Processing {target}...")

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
                'provider': self.settings.extraction.llm_provider,
                'model': self.settings.extraction.ollama_model if self.settings.extraction.llm_provider == 'ollama' else self.settings.extraction.gemini_model,
                'temperature': self.settings.extraction.temperature
            }
        }

    def _execute_parallel(self, targets: List[str], extraction_type: str,
                         extractor: Any, is_domain: bool, force: bool,
                         workers: int) -> Dict[str, Any]:
        """
        Execute extraction in parallel using multiple workers

        Args:
            targets: List of targets to process
            extraction_type: Type of extraction
            extractor: The extractor instance to use
            is_domain: Whether targets are domains
            force: Force extraction even if exists
            workers: Number of parallel workers

        Returns:
            Extraction results
        """
        all_results = []
        start_time = time.time()
        total_targets = len(targets)
        self.completed_count = 0

        def process_single_target(target_info):
            """Process a single target"""
            idx, target = target_info

            try:
                # Check if extraction already exists (unless forced)
                if not force and is_domain and self._extraction_exists(target, extraction_type):
                    with self.progress_lock:
                        self.completed_count += 1
                        print(f"[{self.completed_count}/{total_targets}] Skipping {target} (already extracted)...")

                    return {
                        'target': target,
                        'type': 'domain',
                        'data': {'skipped': True, 'reason': 'Already extracted'}
                    }

                # Perform extraction
                if is_domain:
                    result = extractor.extract_from_domain(target)
                else:
                    result = extractor.extract_from_document(target)

                # Store successful extraction in database (thread-safe)
                if result and not result.get('error'):
                    with self.db_lock:
                        self._store_extraction(target, extraction_type, result, is_domain)

                # Update progress
                with self.progress_lock:
                    self.completed_count += 1
                    elapsed = time.time() - start_time
                    rate = self.completed_count / elapsed if elapsed > 0 else 0
                    remaining = (total_targets - self.completed_count) / rate if rate > 0 else 0

                    status = "✓" if result and not result.get('error') else "✗"
                    print(f"[{self.completed_count}/{total_targets}] {status} {target} "
                          f"({rate:.1f}/s, ~{remaining/60:.1f}m remaining)")

                return {
                    'target': target,
                    'type': 'domain' if is_domain else 'document',
                    'data': result
                }

            except Exception as e:
                logger.error(f"Error processing {target}: {str(e)}")
                with self.progress_lock:
                    self.completed_count += 1
                    print(f"[{self.completed_count}/{total_targets}] ✗ {target} (error)")

                return {
                    'target': target,
                    'type': 'domain' if is_domain else 'document',
                    'data': {'error': str(e)}
                }

        # Process targets in parallel
        print(f"\nProcessing {total_targets} targets with {workers} workers...")
        print(f"{'='*60}\n")

        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Submit all tasks
            futures = {
                executor.submit(process_single_target, (i, target)): target
                for i, target in enumerate(targets, 1)
            }

            # Collect results as they complete
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=30)  # 30 second timeout per domain
                    all_results.append(result)
                except Exception as e:
                    target = futures[future]
                    logger.error(f"Failed to process {target}: {str(e)}")
                    all_results.append({
                        'target': target,
                        'type': 'domain' if is_domain else 'document',
                        'data': {'error': str(e)}
                    })

        # Calculate final statistics
        elapsed_time = time.time() - start_time
        successful = sum(1 for r in all_results if r.get('data') and not r['data'].get('error') and not r['data'].get('skipped'))
        skipped = sum(1 for r in all_results if r.get('data', {}).get('skipped'))
        failed = sum(1 for r in all_results if r.get('data', {}).get('error'))

        print(f"\n{'='*60}")
        print(f"Completed {total_targets} targets in {elapsed_time/60:.1f} minutes")
        print(f"Rate: {total_targets/elapsed_time:.1f} targets/second")
        print(f"Successful: {successful}, Skipped: {skipped}, Failed: {failed}")
        print(f"{'='*60}\n")

        return {
            'extraction_type': extraction_type,
            'targets': targets,
            'target_type': 'domain' if is_domain else 'document',
            'timestamp': datetime.now().isoformat(),
            'results': all_results,
            'summary': {
                'total_targets': total_targets,
                'successful': successful,
                'skipped': skipped,
                'failed': failed,
                'elapsed_time': elapsed_time,
                'workers_used': workers
            },
            'config': {
                'provider': self.settings.extraction.llm_provider,
                'model': self.settings.extraction.ollama_model if self.settings.extraction.llm_provider == 'ollama' else self.settings.extraction.gemini_model,
                'temperature': self.settings.extraction.temperature
            }
        }

    def execute_all(self, extraction_type: str, force: bool = False, workers: int = 1) -> Dict[str, Any]:
        """
        Execute extraction for all domains with embeddings

        Args:
            extraction_type: Type of extraction (specific type or 'all')
            force: Force extraction even if data already exists

        Returns:
            Extraction results
        """
        import psycopg2

        try:
            # Get the appropriate database URI
            if self.db_conn.is_local:
                db_uri = self.settings.database.local_database_uri
            else:
                db_uri = self.settings.database.supabase_database_uri

            if not db_uri:
                raise ValueError("No database URI configured")

            conn = psycopg2.connect(db_uri)
            cur = conn.cursor()

            try:
                # Get domains based on force flag
                if force:
                    # Get all domains that have embeddings
                    logger.info("Getting all domains with embeddings (force mode)...")
                    cur.execute("""
                        SELECT DISTINCT domain
                        FROM document_vectors
                        ORDER BY domain
                    """)
                else:
                    # Get only domains without existing extractions
                    logger.info(f"Getting domains without existing {extraction_type} extractions...")

                    # Build query based on extraction type
                    if extraction_type == 'all':
                        # For 'all', get domains that don't have ALL extraction types
                        # This is complex, so for now just get all domains
                        cur.execute("""
                            SELECT DISTINCT domain
                            FROM document_vectors
                            ORDER BY domain
                        """)
                    else:
                        # Get domains that don't have this specific extraction type
                        cur.execute("""
                            SELECT DISTINCT dv.domain
                            FROM document_vectors dv
                            LEFT JOIN domain_extractions de
                                ON dv.domain = de.domain
                                AND de.extraction_name = %s
                            WHERE de.domain IS NULL
                            ORDER BY dv.domain
                        """, (extraction_type,))

                domains = [row[0] for row in cur.fetchall()]

                if force:
                    logger.info(f"Found {len(domains)} domains with embeddings (processing all)")
                else:
                    logger.info(f"Found {len(domains)} domains needing {extraction_type} extraction")
            finally:
                cur.close()
                conn.close()

            if not domains:
                return {
                    'extraction_type': extraction_type,
                    'total_targets': 0,
                    'successful': 0,
                    'target_type': 'domain',
                    'message': 'No domains with embeddings found',
                    'results': []
                }

            # Execute extraction on all domains
            return self.execute(domains, extraction_type, is_domain=True, force=force, workers=workers)

        except Exception as e:
            logger.error(f"Execute all failed: {str(e)}")
            return {
                'error': str(e),
                'total_targets': 0,
                'successful': 0
            }
    
    def _execute_all_extractors(self, targets: List[str], is_domain: bool, force: bool = False) -> Dict[str, Any]:
        """
        Execute all extractors for the given targets

        Args:
            targets: List of document IDs or domain names
            is_domain: Whether targets are domains or documents
            force: Force extraction even if data already exists

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
                # Check if extraction already exists (unless forced)
                if not force and is_domain and self._extraction_exists(target, extraction_type):
                    logger.info(f"  Skipping {extraction_type} - already exists")
                    target_results['extractions'][extraction_type] = {'skipped': True}
                    continue

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
                'provider': self.settings.extraction.llm_provider,
                'model': self.settings.extraction.ollama_model if self.settings.extraction.llm_provider == 'ollama' else self.settings.extraction.gemini_model,
                'temperature': self.settings.extraction.temperature
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
    
    def _extraction_exists(self, domain: str, extraction_type: str) -> bool:
        """
        Check if an extraction already exists for a domain

        Args:
            domain: Domain name
            extraction_type: Type of extraction

        Returns:
            True if extraction exists, False otherwise
        """
        try:
            with self.db_conn.get_postgres_connection() as (conn, cur):
                cur.execute("""
                    SELECT EXISTS(
                        SELECT 1
                        FROM domain_extractions
                        WHERE domain = %s
                        AND extraction_name = %s
                        LIMIT 1
                    )
                """, (domain, extraction_type))

                return cur.fetchone()[0]
        except Exception as e:
            logger.warning(f"Error checking for existing extraction: {str(e)}")
            # If we can't check, assume it doesn't exist to avoid blocking extraction
            return False

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
                    f"{self.settings.extraction.llm_provider}:{self.settings.extraction.ollama_model if self.settings.extraction.llm_provider == 'ollama' else self.settings.extraction.gemini_model}",  # Use provider:model as version
                    json.dumps(clean_result),
                    datetime.now(),
                    datetime.now(),
                    datetime.now()
                ))
                conn.commit()

                if cur.rowcount > 0:
                    logger.info(f"Stored extraction for {target} in database (ID: {extraction_id})")

                    # Update domain status if this is a law_firm_confirmation
                    if extraction_type == 'law_firm_confirmation' and is_domain:
                        is_law_firm = clean_result.get('is_law_firm', False)
                        is_pi_firm = clean_result.get('is_personal_injury_firm', False)

                        # Check if both are true (handle string or boolean values)
                        if (str(is_law_firm).lower() == 'true' and
                            str(is_pi_firm).lower() == 'true'):

                            # Update crawl_status to 'verified'
                            cur.execute("""
                                UPDATE domains
                                SET crawl_status = 'verified',
                                    updated_at = %s
                                WHERE domain = %s
                            """, (datetime.now(), domain))
                            conn.commit()
                            logger.info(f"Updated {domain} crawl_status to 'verified' (qualified PI law firm)")

                        # If either is false, mark as failed_verification
                        elif (str(is_law_firm).lower() == 'false' or
                              str(is_pi_firm).lower() == 'false'):

                            # Update crawl_status to 'failed_verification'
                            cur.execute("""
                                UPDATE domains
                                SET crawl_status = 'failed_verification',
                                    updated_at = %s
                                WHERE domain = %s
                            """, (datetime.now(), domain))
                            conn.commit()
                            logger.info(f"Updated {domain} crawl_status to 'failed_verification' (not qualified: is_law_firm={is_law_firm}, is_pi_firm={is_pi_firm})")
                else:
                    logger.warning(f"Extraction already exists for {target}")

        except Exception as e:
            logger.error(f"Failed to store extraction: {str(e)}")
            # Don't fail the whole extraction if storage fails
            pass