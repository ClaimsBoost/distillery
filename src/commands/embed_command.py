"""
Embed command handler
Handles document embedding operations
"""

import logging
from typing import List, Dict, Any, Optional

from ..core.settings import get_settings, Settings
from ..embed import DocumentEmbedder
from ..database.connection import get_database_connection

logger = logging.getLogger(__name__)


class EmbedCommand:
    """Handles embed command operations"""
    
    def __init__(self, settings: Settings = None, storage_config: Dict[str, Any] = None):
        """
        Initialize embed command
        
        Args:
            settings: Application settings (uses global if not provided)
            storage_config: Storage configuration (uses settings if not provided)
        """
        self.settings = settings or get_settings()
        self.storage_config = storage_config or {
            'type': self.settings.storage.type,
            'bucket': self.settings.storage.bucket,
            'base_path': self.settings.storage.base_path
        }
        self.embedder = DocumentEmbedder(self.settings, self.storage_config)
    
    def execute(self, targets: List[str], is_domain: bool = False, 
                force: bool = False) -> Dict[str, Any]:
        """
        Execute embed command for multiple targets
        
        Args:
            targets: List of file paths or domain names
            is_domain: Whether targets are domains
            force: Whether to force re-embedding
        
        Returns:
            Embedding results
        """
        all_results = []
        total_chunks = 0
        successful = 0
        
        for target in targets:
            logger.info(f"Embedding target: {target}")
            
            # Perform embedding
            if is_domain:
                result = self.embedder.embed_domain(target, force)
            else:
                result = self.embedder.embed_file(target, force)
            
            # Track results
            if result.get('success'):
                successful += 1
                total_chunks += result.get('total_chunks', 0)
                
                # Add verification for domains
                if is_domain:
                    verification = self.embedder.verify_embeddings(target)
                    result['verification'] = verification
            
            all_results.append({
                'target': target,
                'result': result
            })
        
        # Return summary
        return {
            'targets': targets,
            'type': 'domain' if is_domain else 'file',
            'total_targets': len(targets),
            'successful': successful,
            'total_chunks': total_chunks,
            'results': all_results
        }

    def execute_all(self, force: bool = False) -> Dict[str, Any]:
        """
        Execute embed command for all domains

        Args:
            force: If True, re-embed all domains. If False, only embed pending domains.

        Returns:
            Embedding results
        """
        # Get database connection
        db_conn = get_database_connection()

        if not db_conn.has_connection:
            logger.error("No database connection available")
            return {
                'error': 'No database connection available',
                'total_targets': 0,
                'successful': 0
            }

        try:
            with db_conn.get_postgres_connection() as (conn, cur):
                # Check if domain_paths table exists
                cur.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables
                        WHERE table_name = 'domain_paths'
                    )
                """)
                has_domain_paths = cur.fetchone()[0]

                if has_domain_paths and not force:
                    # Get only domains with pending embeddings
                    logger.info("Getting domains with pending embeddings...")
                    cur.execute("""
                        SELECT DISTINCT domain
                        FROM domain_paths
                        WHERE is_stored = true
                          AND (is_embedded = false OR is_embedded IS NULL)
                        ORDER BY domain
                    """)
                    domains = [row[0] for row in cur.fetchall()]
                    operation_type = "pending"
                else:
                    # Get all domains with stored content
                    logger.info(f"Getting all domains for {'re-' if force else ''}embedding...")
                    if has_domain_paths:
                        cur.execute("""
                            SELECT DISTINCT domain
                            FROM domain_paths
                            WHERE is_stored = true
                            ORDER BY domain
                        """)
                    else:
                        # Fallback to domains table if domain_paths doesn't exist
                        cur.execute("""
                            SELECT DISTINCT domain
                            FROM domains
                            ORDER BY domain
                        """)
                    domains = [row[0] for row in cur.fetchall()]
                    operation_type = "all"

                logger.info(f"Found {len(domains)} domains to process ({operation_type})")

                if not domains:
                    return {
                        'total_targets': 0,
                        'successful': 0,
                        'total_chunks': 0,
                        'type': 'domain',
                        'message': 'No domains to embed',
                        'operation': operation_type,
                        'results': []
                    }

                # Process all domains
                all_results = []
                total_chunks = 0
                successful = 0
                failed_domains = []

                for i, domain in enumerate(domains, 1):
                    logger.info(f"[{i}/{len(domains)}] Embedding domain: {domain}")
                    print(f"[{i}/{len(domains)}] Processing {domain}...")

                    try:
                        result = self.embedder.embed_domain(domain, force)

                        if result.get('success'):
                            successful += 1
                            total_chunks += result.get('total_chunks', 0)

                            # Add verification
                            verification = self.embedder.verify_embeddings(domain)
                            result['verification'] = verification
                        else:
                            failed_domains.append(domain)

                        all_results.append({
                            'target': domain,
                            'result': result
                        })
                    except Exception as e:
                        logger.error(f"Failed to embed {domain}: {str(e)}")
                        failed_domains.append(domain)
                        all_results.append({
                            'target': domain,
                            'result': {'success': False, 'error': str(e)}
                        })

                # Return summary
                return {
                    'targets': domains,
                    'type': 'domain',
                    'operation': operation_type,
                    'force': force,
                    'total_targets': len(domains),
                    'successful': successful,
                    'failed': len(failed_domains),
                    'failed_domains': failed_domains,
                    'total_chunks': total_chunks,
                    'results': all_results
                }

        except Exception as e:
            logger.error(f"Execute all failed: {str(e)}")
            return {
                'error': str(e),
                'total_targets': 0,
                'successful': 0
            }

    def display_results(self, results: Dict[str, Any]):
        """
        Display embedding results

        Args:
            results: Results dictionary from execute()
        """
        print(f"\n{'='*60}")
        print(f"EMBEDDING RESULTS")
        print(f"{'='*60}")

        # Handle error case
        if 'error' in results and results.get('total_targets') == 0:
            print(f"✗ Error: {results['error']}")
            return

        # Handle no domains case
        if 'message' in results and results.get('total_targets') == 0:
            print(f"{results['message']}")
            if 'operation' in results:
                if results['operation'] == 'pending':
                    print("All domains are already embedded. Use --force to re-embed.")
            return

        # Display operation type if available
        if 'operation' in results:
            operation_desc = "all domains" if results['operation'] == 'all' else "pending domains"
            if results.get('force'):
                operation_desc = f"all domains (force re-embed)"
            print(f"Operation: Embed {operation_desc}")

        print(f"Total targets: {results['total_targets']}")
        print(f"Successful: {results['successful']}")

        # Display failed count if present
        if 'failed' in results and results['failed'] > 0:
            print(f"Failed: {results['failed']}")
            if 'failed_domains' in results and results['failed_domains']:
                print(f"Failed domains: {', '.join(results['failed_domains'][:5])}")
                if len(results['failed_domains']) > 5:
                    print(f"  ... and {len(results['failed_domains']) - 5} more")

        print(f"Total chunks embedded: {results['total_chunks']}")
        print(f"Type: {'domains' if results['type'] == 'domain' else 'files'}")
        
        for item in results['results']:
            target = item['target']
            res = item['result']
            
            if res.get('success'):
                print(f"\n✅ {target}:")
                print(f"  Documents: {res.get('documents_processed', 'N/A')}")
                print(f"  Chunks: {res.get('total_chunks', 'N/A')}")
                
                if 'verification' in res:
                    v = res['verification']
                    print(f"  Verified chunks in DB: {v.get('chunk_count', 'N/A')}")
            else:
                print(f"\n❌ {target}:")
                print(f"  Error: {res.get('error', 'Unknown error')}")