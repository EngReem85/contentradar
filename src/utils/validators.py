import re
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

class Validators:
    """Data validators"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_rating(rating: Any) -> bool:
        """Validate rating (0-5)"""
        try:
            rating = float(rating)
            return 0 <= rating <= 5
        except:
            return False
    
    @staticmethod
    def validate_item_id(item_id: str) -> bool:
        """Validate item ID format"""
        if not item_id:
            return False
        # Item IDs should be alphanumeric with underscores
        pattern = r'^[a-zA-Z0-9_]+$'
        return bool(re.match(pattern, item_id))
    
    @staticmethod
    def validate_text(text: str, min_length: int = 1, max_length: int = 10000) -> bool:
        """Validate text length"""
        if not isinstance(text, str):
            return False
        return min_length <= len(text) <= max_length