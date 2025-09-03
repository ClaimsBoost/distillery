"""
Embed command handler
Handles document embedding operations
"""

import logging
from typing import List, Dict, Any, Optional

from ..core.config_manager import ExtractionConfig
from ..embed import DocumentEmbedder

logger = logging.getLogger(__name__)


class EmbedCommand:
    """Handles embed command operations"""
    
    def __init__(self, config: ExtractionConfig, storage_config: Dict[str, Any]):
        """
        Initialize embed command
        
        Args:
            config: Extraction configuration
            storage_config: Storage configuration
        """
        self.config = config
        self.storage_config = storage_config
        self.embedder = DocumentEmbedder(config, storage_config)
    
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
    
    def display_results(self, results: Dict[str, Any]):
        """
        Display embedding results
        
        Args:
            results: Results dictionary from execute()
        """
        print(f"\n{'='*60}")
        print(f"EMBEDDING RESULTS")
        print(f"{'='*60}")
        print(f"Total targets: {results['total_targets']}")
        print(f"Successful: {results['successful']}")
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