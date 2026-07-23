import random
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ABTesting:
    """A/B Testing framework"""
    
    def __init__(self, test_id: str):
        self.test_id = test_id
        self.results = {
            'variant_a': {'views': 0, 'clicks': 0, 'conversions': 0},
            'variant_b': {'views': 0, 'clicks': 0, 'conversions': 0}
        }
        self.user_assignments = {}
    
    def assign_variant(self, user_id: str) -> str:
        """Assign user to a variant"""
        if user_id not in self.user_assignments:
            # Use hash for consistent assignment
            hash_val = hash(f"{user_id}_{self.test_id}") % 2
            variant = 'A' if hash_val == 0 else 'B'
            self.user_assignments[user_id] = variant
            logger.info(f"Assigned user {user_id} to variant {variant}")
        
        return self.user_assignments[user_id]
    
    def track_view(self, user_id: str, variant: str):
        """Track a view"""
        key = f'variant_{variant.lower()}'
        if key in self.results:
            self.results[key]['views'] += 1
    
    def track_click(self, user_id: str, variant: str):
        """Track a click"""
        key = f'variant_{variant.lower()}'
        if key in self.results:
            self.results[key]['clicks'] += 1
    
    def track_conversion(self, user_id: str, variant: str):
        """Track a conversion"""
        key = f'variant_{variant.lower()}'
        if key in self.results:
            self.results[key]['conversions'] += 1
    
    def get_results(self) -> Dict[str, Any]:
        """Get test results"""
        a = self.results['variant_a']
        b = self.results['variant_b']
        
        # Calculate conversion rates
        a_ctr = (a['clicks'] / a['views'] * 100) if a['views'] > 0 else 0
        b_ctr = (b['clicks'] / b['views'] * 100) if b['views'] > 0 else 0
        
        a_conv = (a['conversions'] / a['clicks'] * 100) if a['clicks'] > 0 else 0
        b_conv = (b['conversions'] / b['clicks'] * 100) if b['clicks'] > 0 else 0
        
        return {
            'test_id': self.test_id,
            'variant_a': a,
            'variant_b': b,
            'click_through_rate': {'A': a_ctr, 'B': b_ctr},
            'conversion_rate': {'A': a_conv, 'B': b_conv},
            'winner': 'A' if a_ctr > b_ctr else 'B' if b_ctr > a_ctr else 'Tie',
            'sample_size': a['views'] + b['views']
        }