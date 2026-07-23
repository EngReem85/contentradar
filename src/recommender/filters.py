from typing import List, Dict, Any, Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class FilterEngine:
    """Advanced filtering for recommendations"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def apply_filters(self, results: List[Dict], filters: Dict) -> List[Dict]:
        """Apply filters to results"""
        
        if not results:
            return []
        
        filtered = results.copy()
        
        # Filter by minimum rating
        if 'min_rating' in filters:
            min_rating = filters['min_rating']
            filtered = [
                item for item in filtered 
                if item.get('metadata', {}).get('vote_average', 0) >= min_rating
            ]
        
        # Filter by year range
        if 'year_range' in filters:
            start_year, end_year = filters['year_range']
            filtered = [
                item for item in filtered
                if start_year <= item.get('metadata', {}).get('release_date', '0000')[:4] <= end_year
            ]
        
        # Filter by genres (include)
        if 'genres_include' in filters:
            include_genres = filters['genres_include']
            filtered = [
                item for item in filtered
                if any(g in item.get('genres', []) for g in include_genres)
            ]
        
        # Filter by genres (exclude)
        if 'genres_exclude' in filters:
            exclude_genres = filters['genres_exclude']
            filtered = [
                item for item in filtered
                if not any(g in item.get('genres', []) for g in exclude_genres)
            ]
        
        # Filter by content types
        if 'content_types' in filters:
            content_types = filters['content_types']
            filtered = [
                item for item in filtered
                if item.get('content_type') in content_types
            ]
        
        # Filter by minimum popularity
        if 'min_popularity' in filters:
            min_pop = filters['min_popularity']
            filtered = [
                item for item in filtered
                if item.get('popularity', 0) >= min_pop
            ]
        
        # Exclude specific IDs
        if 'exclude_ids' in filters:
            exclude_ids = filters['exclude_ids']
            filtered = [
                item for item in filtered
                if item.get('id') not in exclude_ids
            ]
        
        logger.info(f"Filtered {len(results)} -> {len(filtered)} items")
        return filtered