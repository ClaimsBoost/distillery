"""
Test command handler
Handles testing office extraction against ground truth
"""

import json
import logging
import time
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..core.settings import get_settings, Settings
from ..core.storage_handler import StorageHandler
from ..extract import OfficeExtractor

logger = logging.getLogger(__name__)


class TestCommand:
    """Handles test-domain command operations"""
    
    def __init__(self, settings: Settings = None, supabase_client=None):
        """
        Initialize test command
        
        Args:
            settings: Application settings (uses global if not provided)
            supabase_client: Optional Supabase client
        """
        self.settings = settings or get_settings()
        self.storage_config = {
            'type': self.settings.storage.type,
            'bucket': self.settings.storage.bucket,
            'base_path': self.settings.storage.base_path
        }
        self.supabase_client = supabase_client
        self.storage = StorageHandler(self.storage_config)
        self.extractor = OfficeExtractor(self.settings, supabase_client)
    
    def execute(self, domain: str, re_embed: bool = False) -> Dict[str, Any]:
        """
        Test office extraction for a domain against ground truth
        
        Args:
            domain: Domain name to test
            re_embed: Whether to re-embed documents
        
        Returns:
            Test results with metrics
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing office extraction for domain: {domain}")
        logger.info(f"{'='*60}")
        
        # Load ground truth
        ground_truth_file = Path('tests/test_data/office_locations_test_set.json')
        if not ground_truth_file.exists():
            logger.error(f"Ground truth file not found: {ground_truth_file}")
            return {'error': 'Ground truth file not found'}
        
        with open(ground_truth_file, 'r') as f:
            ground_truth_data = json.load(f)
        
        # Find ground truth for this domain
        ground_truth_sample = None
        for sample in ground_truth_data['samples']:
            if sample['domain'] == domain:
                ground_truth_sample = sample
                break
        
        if not ground_truth_sample:
            logger.error(f"No ground truth found for domain: {domain}")
            return {'error': f'No ground truth for domain {domain}'}
        
        logger.info(f"Firm: {ground_truth_sample.get('firm_name', 'Unknown')}")
        logger.info(f"Expected offices: {len(ground_truth_sample['ground_truth']['offices'])}")
        
        # Download and combine markdown files
        files = self.storage.list_files_for_domain(domain)
        
        if not files:
            logger.error(f"No markdown files found for domain {domain}")
            return {'error': f'No files found for domain {domain}'}
        
        logger.info(f"Found {len(files)} markdown files")
        
        # Combine content (limit for testing)
        all_content = []
        for filename in files[:10]:  # Limit to first 10 files
            content = self.storage.download_file(domain, filename)
            if content:
                all_content.append(content)
                logger.debug(f"Loaded {filename} ({len(content)} chars)")
        
        combined_content = "\n\n".join(all_content)
        logger.info(f"Combined content: {len(combined_content)} chars from {len(all_content)} files")
        
        # Extract offices
        logger.info(f"Starting extraction (re_embed={re_embed})...")
        start_time = time.time()
        
        try:
            # Set re_embed flag if needed
            if hasattr(self.extractor, 're_embed'):
                self.extractor.re_embed = re_embed
            
            # Extract offices
            metadata = {
                'domain': domain,
                'source': f"{domain}/combined"
            }
            extracted_data = self.extractor.extract(combined_content, metadata)
            
            extraction_time = time.time() - start_time
            logger.info(f"Extraction completed in {extraction_time:.2f} seconds")
            
            # Get offices from extracted data
            extracted_offices = extracted_data.get('offices', [])
            
            # Compare with ground truth
            comparison = self._compare_offices(
                extracted_offices,
                ground_truth_sample['ground_truth']['offices']
            )
            
            # Calculate metrics
            metrics = self._calculate_metrics(comparison)
            
            # Prepare results
            result = {
                'domain': domain,
                'firm_name': ground_truth_sample.get('firm_name'),
                'success': True,
                'extraction_time': extraction_time,
                'extracted_offices': extracted_offices,
                'ground_truth': ground_truth_sample['ground_truth'],
                'comparison': comparison,
                'metrics': metrics
            }
            
            # Display results
            self.display_results(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            return {
                'domain': domain,
                'success': False,
                'error': str(e)
            }
    
    def _compare_offices(self, extracted: List[Dict], ground_truth: List[Dict]) -> Dict[str, Any]:
        """Compare extracted offices with ground truth"""
        comparison = {
            'matched': [],
            'partial_matches': [],
            'missing': [],
            'extra': []
        }
        
        # Normalize function
        def normalize_office(office):
            if isinstance(office, dict):
                if 'address' in office:
                    addr = office['address']
                    return {
                        'city': addr.get('city', '').lower().strip(),
                        'state': addr.get('state', '').upper().strip(),
                        'street': addr.get('street', '').lower().strip(),
                        'original': office
                    }
            return None
        
        # Normalize offices
        extracted_norm = [normalize_office(o) for o in extracted if normalize_office(o)]
        gt_norm = [normalize_office(o) for o in ground_truth if normalize_office(o)]
        
        # Track matched ground truth indices
        matched_gt = set()
        
        # Find matches
        for ext in extracted_norm:
            matched = False
            for i, gt in enumerate(gt_norm):
                if i in matched_gt:
                    continue
                
                # Exact city+state match
                if ext['city'] == gt['city'] and ext['state'] == gt['state']:
                    comparison['matched'].append({
                        'extracted': ext['original'],
                        'ground_truth': gt['original']
                    })
                    matched_gt.add(i)
                    matched = True
                    break
                # Partial match (city only)
                elif ext['city'] == gt['city']:
                    comparison['partial_matches'].append({
                        'extracted': ext['original'],
                        'ground_truth': gt['original']
                    })
                    matched_gt.add(i)
                    matched = True
                    break
            
            if not matched:
                comparison['extra'].append(ext['original'])
        
        # Find missing
        for i, gt in enumerate(gt_norm):
            if i not in matched_gt:
                comparison['missing'].append(gt['original'])
        
        return comparison
    
    def _calculate_metrics(self, comparison: Dict[str, Any]) -> Dict[str, float]:
        """Calculate precision, recall, and F1 score"""
        total_extracted = len(comparison['matched']) + len(comparison['extra']) + len(comparison['partial_matches'])
        total_ground_truth = len(comparison['matched']) + len(comparison['missing']) + len(comparison['partial_matches'])
        
        # Count with partial credit
        matched_count = len(comparison['matched']) + (0.5 * len(comparison['partial_matches']))
        
        precision = matched_count / total_extracted if total_extracted > 0 else 0
        recall = matched_count / total_ground_truth if total_ground_truth > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'exact_matches': len(comparison['matched']),
            'partial_matches': len(comparison['partial_matches']),
            'missing': len(comparison['missing']),
            'extra': len(comparison['extra'])
        }
    
    def display_results(self, result: Dict[str, Any]):
        """Display test results in readable format"""
        print(f"\n{'='*60}")
        print(f"Results for: {result['domain']} - {result.get('firm_name', 'Unknown')}")
        print(f"{'='*60}")
        
        if not result['success']:
            print(f"❌ ERROR: {result.get('error', 'Unknown error')}")
            return
        
        metrics = result['metrics']
        print(f"\n📊 METRICS:")
        print(f"  Precision: {metrics['precision']:.2%}")
        print(f"  Recall: {metrics['recall']:.2%}")
        print(f"  F1 Score: {metrics['f1_score']:.2%}")
        
        print(f"\n📍 OFFICE COUNTS:")
        print(f"  Exact Matches: {metrics['exact_matches']}")
        print(f"  Partial Matches: {metrics['partial_matches']}")
        print(f"  Missing: {metrics['missing']}")
        print(f"  Extra: {metrics['extra']}")
        
        comparison = result['comparison']
        
        if comparison['matched']:
            print(f"\n✅ MATCHED OFFICES:")
            for match in comparison['matched']:
                gt = match['ground_truth']['address']
                print(f"  - {gt['city']}, {gt['state']}")
        
        if comparison['missing']:
            print(f"\n❌ MISSING OFFICES:")
            for office in comparison['missing']:
                addr = office['address']
                print(f"  - {addr['city']}, {addr['state']}")
    
    def save_results(self, result: Dict[str, Any], output_path: str):
        """Save test results to file"""
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to {output_path}")