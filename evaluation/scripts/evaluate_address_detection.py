#!/usr/bin/env python3
"""
Evaluate address detection algorithm performance
Compares pattern detection results against ground truth
"""

import json
import os
import psycopg2
from psycopg2.extras import DictCursor
from typing import Dict, List, Set, Tuple
import re
from datetime import datetime


class AddressDetectionEvaluator:
    """Evaluates address detection pattern performance"""
    
    def __init__(self):
        """Initialize evaluator"""
        self.db_url = os.environ.get('LOCAL_DATABASE_URL', 'postgresql://localhost:5432/distillery')
        self.conn = psycopg2.connect(self.db_url)
        
    def load_ground_truth(self, test_set_path: str = "evaluation/test_data/office_locations_test_set.json") -> Dict:
        """Load ground truth addresses from test set"""
        with open(test_set_path, 'r') as f:
            data = json.load(f)
        
        # Create dict of domain -> addresses
        ground_truth = {}
        for sample in data['samples']:
            domain = sample['domain']
            addresses = sample['ground_truth']['offices']
            ground_truth[domain] = addresses
        
        return ground_truth
    
    def normalize_address_for_matching(self, address: str) -> str:
        """Normalize address for fuzzy matching"""
        # Convert to lowercase and remove punctuation
        normalized = address.lower()
        normalized = re.sub(r'[.,;:#\-\(\)]', ' ', normalized)
        # Remove extra spaces
        normalized = ' '.join(normalized.split())
        return normalized
    
    def check_chunk_contains_address(self, chunk_content: str, addresses: List[str]) -> bool:
        """Check if a chunk contains any of the ground truth addresses"""
        chunk_normalized = self.normalize_address_for_matching(chunk_content)
        
        for address in addresses:
            # Extract key parts of address for matching
            # Since addresses might be formatted differently, look for key components
            address_parts = self.normalize_address_for_matching(address).split()
            
            # Check if majority of address parts are in chunk
            # Need at least street number and name
            matches = 0
            for part in address_parts:
                if len(part) > 2 and part in chunk_normalized:  # Skip short words like "st"
                    matches += 1
            
            # If we match at least 60% of address parts, consider it a match
            if matches >= len(address_parts) * 0.6:
                return True
        
        return False
    
    def evaluate_domain(self, domain: str, ground_truth_addresses: List[str]) -> Dict:
        """Evaluate address detection for a single domain"""
        
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            # Get all chunks for this domain
            cur.execute("""
                SELECT 
                    id,
                    content,
                    metadata->>'contains_addresses' as marked_has_address,
                    metadata->>'address_count' as address_count
                FROM document_vectors 
                WHERE metadata->>'domain' = %s
            """, (domain,))
            
            chunks = cur.fetchall()
            
            if not chunks:
                return {
                    'domain': domain,
                    'error': 'No chunks found in database',
                    'total_chunks': 0
                }
            
            # Categorize chunks
            true_positives = []  # Marked as address and contains address
            false_positives = [] # Marked as address but no address
            true_negatives = []  # Not marked and no address
            false_negatives = [] # Not marked but contains address
            
            for chunk in chunks:
                chunk_id = chunk['id']
                content = chunk['content']
                marked_has_address = chunk['marked_has_address'] == 'true'
                
                # Check if chunk actually contains a ground truth address
                actually_has_address = self.check_chunk_contains_address(content, ground_truth_addresses)
                
                if marked_has_address and actually_has_address:
                    true_positives.append({
                        'id': chunk_id,
                        'preview': content[:200] + '...' if len(content) > 200 else content
                    })
                elif marked_has_address and not actually_has_address:
                    false_positives.append({
                        'id': chunk_id,
                        'preview': content[:200] + '...' if len(content) > 200 else content
                    })
                elif not marked_has_address and not actually_has_address:
                    true_negatives.append(chunk_id)
                else:  # not marked but has address
                    false_negatives.append({
                        'id': chunk_id,
                        'preview': content[:200] + '...' if len(content) > 200 else content
                    })
            
            # Calculate metrics
            tp = len(true_positives)
            fp = len(false_positives)
            tn = len(true_negatives)
            fn = len(false_negatives)
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
            
            return {
                'domain': domain,
                'total_chunks': len(chunks),
                'ground_truth_addresses': ground_truth_addresses,
                'true_positives': tp,
                'false_positives': fp,
                'true_negatives': tn,
                'false_negatives': fn,
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score,
                'accuracy': accuracy,
                'tp_examples': true_positives[:3],  # Show first 3 examples
                'fp_examples': false_positives[:3],
                'fn_examples': false_negatives[:3]
            }
    
    def evaluate_all(self) -> Dict:
        """Evaluate all test domains"""
        ground_truth = self.load_ground_truth()
        results = {}
        
        # Track overall metrics
        total_tp = 0
        total_fp = 0
        total_tn = 0
        total_fn = 0
        
        for domain, addresses in ground_truth.items():
            print(f"Evaluating {domain}...")
            domain_results = self.evaluate_domain(domain, addresses)
            results[domain] = domain_results
            
            if 'error' not in domain_results:
                total_tp += domain_results['true_positives']
                total_fp += domain_results['false_positives']
                total_tn += domain_results['true_negatives']
                total_fn += domain_results['false_negatives']
        
        # Calculate overall metrics
        overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
        overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
        overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0
        overall_accuracy = (total_tp + total_tn) / (total_tp + total_tn + total_fp + total_fn) if (total_tp + total_tn + total_fp + total_fn) > 0 else 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'domains': results,
            'overall_metrics': {
                'total_true_positives': total_tp,
                'total_false_positives': total_fp,
                'total_true_negatives': total_tn,
                'total_false_negatives': total_fn,
                'precision': overall_precision,
                'recall': overall_recall,
                'f1_score': overall_f1,
                'accuracy': overall_accuracy
            }
        }
    
    def print_summary(self, results: Dict):
        """Print summary of evaluation results"""
        print("\n" + "="*60)
        print("ADDRESS DETECTION EVALUATION RESULTS")
        print("="*60)
        
        # Overall metrics
        overall = results['overall_metrics']
        print(f"\nOVERALL PERFORMANCE:")
        print(f"  Precision: {overall['precision']:.2%} (What % of detected addresses are real)")
        print(f"  Recall: {overall['recall']:.2%} (What % of real addresses were detected)")
        print(f"  F1 Score: {overall['f1_score']:.2%}")
        print(f"  Accuracy: {overall['accuracy']:.2%}")
        
        print(f"\nCONFUSION MATRIX TOTALS:")
        print(f"  True Positives: {overall['total_true_positives']}")
        print(f"  False Positives: {overall['total_false_positives']}")
        print(f"  True Negatives: {overall['total_true_negatives']}")
        print(f"  False Negatives: {overall['total_false_negatives']}")
        
        # Per-domain results
        print(f"\nPER-DOMAIN RESULTS:")
        print("-"*60)
        for domain, metrics in results['domains'].items():
            if 'error' in metrics:
                print(f"{domain}: ERROR - {metrics['error']}")
            else:
                print(f"{domain}:")
                print(f"  Chunks: {metrics['total_chunks']}")
                print(f"  Precision: {metrics['precision']:.2%}, Recall: {metrics['recall']:.2%}, F1: {metrics['f1_score']:.2%}")
                print(f"  TP:{metrics['true_positives']} FP:{metrics['false_positives']} TN:{metrics['true_negatives']} FN:{metrics['false_negatives']}")
                
                # Show examples of failures
                if metrics['false_positives'] > 0:
                    print(f"  False Positive Example: {metrics['fp_examples'][0]['preview'][:100]}...")
                if metrics['false_negatives'] > 0:
                    print(f"  False Negative Example: {metrics['fn_examples'][0]['preview'][:100]}...")
        
        print("="*60)
    
    def close(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    evaluator = AddressDetectionEvaluator()
    
    try:
        results = evaluator.evaluate_all()
        
        # Save results to file
        output_file = f"evaluation/address_detection_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Print summary
        evaluator.print_summary(results)
        print(f"\nDetailed results saved to: {output_file}")
        
    finally:
        evaluator.close()