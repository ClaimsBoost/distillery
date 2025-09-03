#!/usr/bin/env python3
"""
Universal evaluation script for comparing extraction results with ground truth.
Supports multiple extraction types and both test/validation datasets.
"""

import json
import logging
import os
import argparse
from datetime import datetime
from typing import Dict, Any, List, Optional, Set
import psycopg2
from psycopg2.extras import Json
import re
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UniversalEvaluator:
    """Universal evaluator for different extraction types"""
    
    # State abbreviations for normalization
    STATE_ABBR = {
        'alabama': 'al', 'alaska': 'ak', 'arizona': 'az', 'arkansas': 'ar',
        'california': 'ca', 'colorado': 'co', 'connecticut': 'ct', 'delaware': 'de',
        'florida': 'fl', 'georgia': 'ga', 'hawaii': 'hi', 'idaho': 'id',
        'illinois': 'il', 'indiana': 'in', 'iowa': 'ia', 'kansas': 'ks',
        'kentucky': 'ky', 'louisiana': 'la', 'maine': 'me', 'maryland': 'md',
        'massachusetts': 'ma', 'michigan': 'mi', 'minnesota': 'mn', 'mississippi': 'ms',
        'missouri': 'mo', 'montana': 'mt', 'nebraska': 'ne', 'nevada': 'nv',
        'new hampshire': 'nh', 'new jersey': 'nj', 'new mexico': 'nm', 'new york': 'ny',
        'north carolina': 'nc', 'north dakota': 'nd', 'ohio': 'oh', 'oklahoma': 'ok',
        'oregon': 'or', 'pennsylvania': 'pa', 'rhode island': 'ri', 'south carolina': 'sc',
        'south dakota': 'sd', 'tennessee': 'tn', 'texas': 'tx', 'utah': 'ut',
        'vermont': 'vt', 'virginia': 'va', 'washington': 'wa', 'west virginia': 'wv',
        'wisconsin': 'wi', 'wyoming': 'wy'
    }
    
    def __init__(self, extraction_type: str = 'office_locations', 
                 dataset_type: str = 'test', 
                 db_url: Optional[str] = None):
        """
        Initialize evaluator
        
        Args:
            extraction_type: Type of extraction (office_locations, phone_numbers, etc.)
            dataset_type: Either 'test' or 'validation'
            db_url: Database URL for saving results
        """
        self.extraction_type = extraction_type
        self.dataset_type = dataset_type
        self.db_url = db_url or os.environ.get('LOCAL_DATABASE_URL', 
                                                'postgresql://localhost:5432/distillery')
        
        # Build paths based on extraction and dataset type
        self.dataset_path = self._get_dataset_path()
        
        logger.info(f"Initialized evaluator for {extraction_type} using {dataset_type} set")
        
    def _get_dataset_path(self) -> str:
        """Get the path to the appropriate dataset file"""
        base_path = Path("evaluation/test_data")
        filename = f"{self.extraction_type}_{self.dataset_type}_set.json"
        full_path = base_path / filename
        
        if not full_path.exists():
            raise FileNotFoundError(f"Dataset not found: {full_path}")
        
        return str(full_path)
    
    def load_dataset(self) -> Dict:
        """Load the ground truth dataset"""
        logger.info(f"Loading dataset from {self.dataset_path}")
        with open(self.dataset_path, 'r') as f:
            return json.load(f)
    
    def load_extraction_results(self, extraction_file: str) -> Dict[str, Any]:
        """
        Load extraction results from a JSON file
        
        Args:
            extraction_file: Path to extraction results JSON
            
        Returns:
            Dictionary mapping domain to extraction results
        """
        with open(extraction_file, 'r') as f:
            data = json.load(f)
        
        # Convert to format expected by evaluation
        results_by_domain = {}
        
        # Handle different possible formats
        if 'results' in data:
            # Standard format from extraction command
            for result in data.get('results', []):
                domain = result.get('target', '')
                # Keep domain as-is (with dots)
                results_by_domain[domain] = result.get('data', {})
        else:
            # Direct domain mapping format
            results_by_domain = data
        
        logger.info(f"Loaded extraction results for {len(results_by_domain)} domains")
        return results_by_domain
    
    def normalize_value(self, value: str, value_type: str = 'address') -> str:
        """
        Normalize values for comparison based on type
        
        Args:
            value: The value to normalize
            value_type: Type of value (address, phone, email, etc.)
            
        Returns:
            Normalized value string
        """
        if value_type == 'address':
            return self._normalize_address(value)
        elif value_type == 'phone':
            return self._normalize_phone(value)
        elif value_type == 'email':
            return value.lower().strip()
        else:
            return value.lower().strip()
    
    def _normalize_address(self, address_str: str) -> str:
        """Normalize address string for flexible comparison"""
        # Convert to lowercase
        normalized = address_str.lower()
        
        # Remove common punctuation but keep spaces
        normalized = re.sub(r'[.,;:#\-\(\)]', ' ', normalized)
        
        # Standardize common abbreviations
        abbreviations = {
            r'\bste\b': 'suite',
            r'\bst\b': 'street',
            r'\brd\b': 'road',
            r'\bdr\b': 'drive',
            r'\bave\b': 'avenue',
            r'\blane\b': 'ln',
            r'\bblvd\b': 'boulevard',
            r'\bhwy\b': 'highway',
            r'\bpkwy\b': 'parkway',
            r'\btwp\b': 'township',
            r'\bfl\b': 'floor',
            r'\bplz\b': 'plaza'
        }
        
        for pattern, replacement in abbreviations.items():
            normalized = re.sub(pattern, replacement, normalized)
        
        # Replace state names with abbreviations
        for full_state, abbr in self.STATE_ABBR.items():
            normalized = re.sub(r'\b' + full_state + r'\b', abbr, normalized)
        
        # Remove extra spaces
        normalized = ' '.join(normalized.split())
        
        return normalized
    
    def _normalize_phone(self, phone_str: str) -> str:
        """Normalize phone number for comparison"""
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone_str)
        
        # Remove leading 1 if present (US country code)
        if digits_only.startswith('1') and len(digits_only) == 11:
            digits_only = digits_only[1:]
        
        return digits_only
    
    def calculate_metrics(self, extracted: Dict, ground_truth: Dict) -> Dict[str, Any]:
        """
        Calculate evaluation metrics for any extraction type
        
        Args:
            extracted: Extracted data
            ground_truth: Ground truth data
            
        Returns:
            Dictionary of metrics
        """
        # Determine the data field based on extraction type
        data_field = self._get_data_field()
        
        extracted_items = extracted.get(data_field, [])
        truth_items = ground_truth.get(data_field, [])
        
        # Normalize items based on extraction type
        value_type = self._get_value_type()
        
        # Handle both string lists and dict lists
        extracted_normalized = self._normalize_items(extracted_items, value_type)
        truth_normalized = self._normalize_items(truth_items, value_type)
        
        # Calculate exact matches
        correct = extracted_normalized & truth_normalized
        
        # For addresses, also check substring matches
        if value_type == 'address':
            correct = self._check_substring_matches(extracted_normalized, truth_normalized, correct)
        
        # Calculate metrics
        precision = len(correct) / len(extracted_normalized) if extracted_normalized else 0.0
        recall = len(correct) / len(truth_normalized) if truth_normalized else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        # Calculate partial matches for addresses
        partial_matches = 0
        if value_type == 'address':
            partial_matches = self._calculate_partial_matches(
                extracted_normalized, truth_normalized, correct
            )
        
        return {
            'extraction_type': self.extraction_type,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'exact_matches': len(correct),
            'partial_matches': partial_matches,
            'extracted_count': len(extracted_items),
            'truth_count': len(truth_items),
            'false_positives': len(extracted_normalized - truth_normalized),
            'false_negatives': len(truth_normalized - extracted_normalized),
            'extracted_items': list(extracted_normalized),
            'truth_items': list(truth_normalized),
            'correct_items': list(correct)
        }
    
    def _get_data_field(self) -> str:
        """Get the data field name based on extraction type"""
        field_mapping = {
            'office_locations': 'offices',
            'phone_numbers': 'phones',
            'email_addresses': 'emails',
            'practice_areas': 'practice_areas',
            'attorney_names': 'attorneys'
        }
        return field_mapping.get(self.extraction_type, self.extraction_type)
    
    def _get_value_type(self) -> str:
        """Get the value type for normalization"""
        type_mapping = {
            'office_locations': 'address',
            'phone_numbers': 'phone',
            'email_addresses': 'email',
            'practice_areas': 'text',
            'attorney_names': 'text'
        }
        return type_mapping.get(self.extraction_type, 'text')
    
    def _normalize_items(self, items: List, value_type: str) -> Set[str]:
        """Normalize a list of items based on their type"""
        normalized = set()
        
        for item in items:
            if isinstance(item, str):
                # Direct string value
                normalized.add(self.normalize_value(item, value_type))
            elif isinstance(item, dict):
                # Dictionary with structured data
                if 'address' in item:
                    # Old format for addresses
                    addr = item['address']
                    addr_str = f"{addr.get('street', '')} {addr.get('city', '')} {addr.get('state', '')} {addr.get('zip', '')}"
                    normalized.add(self.normalize_value(addr_str, value_type))
                elif 'phone' in item:
                    normalized.add(self.normalize_value(item['phone'], 'phone'))
                elif 'email' in item:
                    normalized.add(self.normalize_value(item['email'], 'email'))
                else:
                    # Try to get any string value from dict
                    for key, val in item.items():
                        if isinstance(val, str):
                            normalized.add(self.normalize_value(val, value_type))
                            break
        
        return normalized
    
    def _check_substring_matches(self, extracted: Set[str], truth: Set[str], 
                                 correct: Set[str]) -> Set[str]:
        """Check for substring matches (for addresses with building names, etc.)"""
        for truth_addr in truth:
            if truth_addr not in correct:
                for ext_addr in extracted:
                    if truth_addr in ext_addr or ext_addr in truth_addr:
                        correct.add(truth_addr)
                        break
        return correct
    
    def _calculate_partial_matches(self, extracted: Set[str], truth: Set[str], 
                                   correct: Set[str]) -> int:
        """Calculate partial matches for addresses"""
        partial_matches = 0
        
        for ext_addr in extracted:
            if ext_addr in correct:
                continue
                
            # Extract city and state from normalized address
            parts = ext_addr.split()
            if len(parts) >= 2:
                for truth_addr in truth:
                    if ext_addr not in correct:
                        # Check for significant overlap
                        ext_words = set(ext_addr.split())
                        truth_words = set(truth_addr.split())
                        common_words = ext_words & truth_words
                        
                        if len(common_words) >= 3:  # At least 3 common words
                            partial_matches += 1
                            break
        
        return partial_matches
    
    def save_results(self, results: Dict[str, Any]):
        """Save evaluation results to database"""
        conn = psycopg2.connect(self.db_url)
        cur = conn.cursor()
        
        try:
            # Create table if not exists (generic for any extraction type)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS extraction_evaluations (
                    id SERIAL PRIMARY KEY,
                    extraction_type VARCHAR(100) NOT NULL,
                    dataset_type VARCHAR(20) NOT NULL,
                    domain VARCHAR(255) NOT NULL,
                    evaluation_timestamp TIMESTAMP DEFAULT NOW(),
                    config_params JSONB,
                    extracted_data JSONB NOT NULL,
                    ground_truth JSONB NOT NULL,
                    metrics JSONB NOT NULL,
                    success BOOLEAN,
                    error_message TEXT
                )
            """)
            
            # Insert results
            for domain, result in results.items():
                cur.execute("""
                    INSERT INTO extraction_evaluations 
                    (extraction_type, dataset_type, domain, config_params,
                     extracted_data, ground_truth, metrics, success, error_message)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    self.extraction_type,
                    self.dataset_type,
                    domain,
                    Json(result.get('config', {})),
                    Json(result['extracted']),
                    Json(result['ground_truth']),
                    Json(result['metrics']),
                    result.get('success', True),
                    result.get('error')
                ))
            
            conn.commit()
            logger.info(f"Saved {len(results)} evaluation results to database")
            
        except Exception as e:
            logger.error(f"Database error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    
    def compare_results(self, extraction_file: str, 
                       domains: Optional[List[str]] = None,
                       save_to_db: bool = True,
                       verbose: bool = True) -> Dict[str, Any]:
        """
        Compare extraction results with ground truth
        
        Args:
            extraction_file: Path to extraction results
            domains: Optional list of specific domains to evaluate
            save_to_db: Whether to save results to database
            verbose: Whether to print detailed output
            
        Returns:
            Dictionary of evaluation results
        """
        # Load dataset
        dataset = self.load_dataset()
        
        # Load extraction results
        extraction_results = self.load_extraction_results(extraction_file)
        
        # Get samples to compare
        if domains:
            # Keep domains as-is
            samples = [s for s in dataset['samples'] if s['domain'] in domains]
        else:
            samples = dataset['samples']
        
        logger.info(f"\nEvaluating {len(samples)} domains for {self.extraction_type}")
        logger.info("=" * 60)
        
        results = {}
        total_metrics = {
            'precision': [],
            'recall': [],
            'f1_score': []
        }
        
        for sample in samples:
            domain = sample['domain']
            ground_truth = sample['ground_truth']
            
            if verbose:
                logger.info(f"\nDomain: {domain}")
                logger.info("-" * 40)
            
            # Get extracted data for this domain
            if domain in extraction_results:
                extracted_data = extraction_results[domain]
                
                # Calculate metrics
                try:
                    metrics = self.calculate_metrics(extracted_data, ground_truth)
                    
                    # Store for averaging
                    total_metrics['precision'].append(metrics['precision'])
                    total_metrics['recall'].append(metrics['recall'])
                    total_metrics['f1_score'].append(metrics['f1_score'])
                    
                    if verbose:
                        logger.info(f"  Extracted: {metrics['extracted_count']} items")
                        logger.info(f"  Ground Truth: {metrics['truth_count']} items")
                        logger.info(f"  Exact Matches: {metrics['exact_matches']}")
                        if metrics.get('partial_matches', 0) > 0:
                            logger.info(f"  Partial Matches: {metrics['partial_matches']}")
                        logger.info(f"  Precision: {metrics['precision']:.2%}")
                        logger.info(f"  Recall: {metrics['recall']:.2%}")
                        logger.info(f"  F1 Score: {metrics['f1_score']:.2%}")
                    
                    results[domain] = {
                        'extracted': extracted_data,
                        'ground_truth': ground_truth,
                        'metrics': metrics,
                        'success': True
                    }
                    
                except Exception as e:
                    logger.error(f"  Error calculating metrics: {str(e)}")
                    results[domain] = {
                        'extracted': extracted_data,
                        'ground_truth': ground_truth,
                        'metrics': {
                            'precision': 0.0,
                            'recall': 0.0,
                            'f1_score': 0.0,
                            'error': str(e)
                        },
                        'success': False,
                        'error': str(e)
                    }
            else:
                if verbose:
                    logger.warning(f"  No extraction results found")
                
                results[domain] = {
                    'extracted': {},
                    'ground_truth': ground_truth,
                    'metrics': {
                        'precision': 0.0,
                        'recall': 0.0,
                        'f1_score': 0.0,
                        'extracted_count': 0,
                        'truth_count': len(ground_truth.get(self._get_data_field(), [])),
                        'error': 'No extraction results found'
                    },
                    'success': False,
                    'error': 'No extraction results found'
                }
        
        # Calculate average metrics
        summary = {}
        if total_metrics['precision']:
            avg_precision = sum(total_metrics['precision']) / len(total_metrics['precision'])
            avg_recall = sum(total_metrics['recall']) / len(total_metrics['recall'])
            avg_f1 = sum(total_metrics['f1_score']) / len(total_metrics['f1_score'])
            
            summary = {
                'avg_precision': avg_precision,
                'avg_recall': avg_recall,
                'avg_f1_score': avg_f1,
                'total_domains': len(samples),
                'successful_domains': len(total_metrics['precision'])
            }
            
            logger.info("\n" + "=" * 60)
            logger.info("OVERALL PERFORMANCE")
            logger.info("=" * 60)
            logger.info(f"Extraction Type: {self.extraction_type}")
            logger.info(f"Dataset Type: {self.dataset_type}")
            logger.info(f"Total Domains: {summary['total_domains']}")
            logger.info(f"Successfully Evaluated: {summary['successful_domains']}")
            logger.info(f"Average Precision: {avg_precision:.2%}")
            logger.info(f"Average Recall: {avg_recall:.2%}")
            logger.info(f"Average F1 Score: {avg_f1:.2%}")
        
        # Save to database if requested
        if save_to_db:
            self.save_results(results)
        
        # Add summary to results
        full_results = {
            'metadata': {
                'extraction_type': self.extraction_type,
                'dataset_type': self.dataset_type,
                'timestamp': datetime.now().isoformat(),
                'extraction_file': extraction_file
            },
            'summary': summary,
            'results': results
        }
        
        return full_results


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        description="Evaluate extraction results against ground truth datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate office locations using test set
  %(prog)s evaluation/results/extractions/office_extraction.json
  
  # Evaluate phone numbers using validation set
  %(prog)s --type phone_numbers --dataset validation phone_extraction.json
  
  # Evaluate specific domains only
  %(prog)s --domains 866attylaw.com 1emslegal.com extraction.json
  
  # Save output to file and skip database
  %(prog)s --output results.json --no-db extraction.json
        """
    )
    
    parser.add_argument(
        'extraction_file',
        help='Path to extraction results JSON file'
    )
    
    parser.add_argument(
        '--type',
        default='office_locations',
        choices=['office_locations', 'phone_numbers', 'email_addresses', 
                'practice_areas', 'attorney_names'],
        help='Type of extraction to evaluate (default: office_locations)'
    )
    
    parser.add_argument(
        '--dataset',
        default='test',
        choices=['test', 'validation'],
        help='Dataset to use for evaluation (default: test)'
    )
    
    parser.add_argument(
        '--domains',
        nargs='+',
        help='Specific domains to evaluate (evaluates all if not specified)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file for results (JSON format)'
    )
    
    parser.add_argument(
        '--no-db',
        action='store_true',
        help='Skip saving results to database'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Reduce output verbosity'
    )
    
    args = parser.parse_args()
    
    # Initialize evaluator
    try:
        evaluator = UniversalEvaluator(
            extraction_type=args.type,
            dataset_type=args.dataset
        )
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        logger.error(f"Make sure you have a {args.type}_{args.dataset}_set.json file in evaluation/test_data/")
        return 1
    
    # Run evaluation
    results = evaluator.compare_results(
        extraction_file=args.extraction_file,
        domains=args.domains,
        save_to_db=not args.no_db,
        verbose=not args.quiet
    )
    
    # Save to output file if specified
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"\nResults saved to {output_path}")
    else:
        # Default output location
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"evaluation/results/evaluations/{args.type}_evaluation_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"\nResults saved to {output_file}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())