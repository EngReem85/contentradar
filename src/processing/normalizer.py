import pandas as pd
import numpy as np
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataNormalizer:
    """Normalize data for analysis"""
    
    @staticmethod
    def normalize_popularity(df: pd.DataFrame, column: str = 'popularity') -> pd.DataFrame:
        """Normalize popularity to 0-1 range"""
        if column not in df.columns:
            return df
        
        min_val = df[column].min()
        max_val = df[column].max()
        
        if max_val - min_val > 0:
            df[f'{column}_normalized'] = (df[column] - min_val) / (max_val - min_val)
        else:
            df[f'{column}_normalized'] = 0
        
        return df
    
    @staticmethod
    def create_text_features(df: pd.DataFrame) -> pd.DataFrame:
        """Create combined text features"""
        def combine(row):
            title = str(row.get('title', ''))
            description = str(row.get('description', ''))
            genres = ' '.join(row.get('genres', [])) if isinstance(row.get('genres'), list) else ''
            content_type = str(row.get('content_type', ''))
            source = str(row.get('source', ''))
            
            return f"{title}. {description}. Genres: {genres}. Type: {content_type}. Source: {source}"
        
        df['text_features'] = df.apply(combine, axis=1)
        return df
    
    @staticmethod
    def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Apply all normalizations"""
        logger.info("Normalizing dataframe...")
        
        df = DataNormalizer.normalize_popularity(df)
        df = DataNormalizer.create_text_features(df)
        
        logger.info(f"Normalized dataframe: {len(df)} rows")
        return df