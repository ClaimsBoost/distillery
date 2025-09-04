"""
Extract command handler
Handles office location extraction from embedded documents
"""

import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..core.config_manager import ExtractionConfig
from ..extract import OfficeExtractor
from ..extract.law_firm_confirmation_extractor import LawFirmConfirmationExtractor
from ..database import get_database_connection

logger = logging.getLogger(__name__)


class ExtractCommand:
    """Handles extract command operations"""
    
    def __init__(self, config: ExtractionConfig, supabase_client=None):
        """
        Initialize extract command
        
        Args:
            config: Extraction configuration
            supabase_client: Optional Supabase client
        """
        self.config = config
        self.supabase_client = supabase_client
        self.extractors = {
            'office_locations': OfficeExtractor(config, supabase_client),
            'law_firm_confirmation': LawFirmConfirmationExtractor(config, supabase_client),
            'short_description': LawFirmConfirmationExtractor(config, supabase_client)  # Legacy alias
        }
    
    def execute(self, targets: List[str], extraction_type: str,
                is_domain: bool = False) -> Dict[str, Any]:
        """
        Execute extraction for multiple targets
        
        Args:
            targets: List of document IDs or domain names
            extraction_type: Type of extraction ('office_locations' or 'short_description')
            is_domain: Whether targets are domains or documents
        
        Returns:
            Extraction results
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Extracting {extraction_type} from {len(targets)} {'domains' if is_domain else 'documents'}")
        logger.info(f"{'='*60}")
        
        # Get the appropriate extractor
        if extraction_type not in self.extractors:
            raise ValueError(f"Unknown extraction type: {extraction_type}. Supported types: {list(self.extractors.keys())}")
        
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
                'model': self.config.model_type,
                'temperature': self.config.temperature,
                'k_chunks': self.config.k_chunks
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