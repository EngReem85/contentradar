import re
import pandas as pd
from typing import List, Any
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    """Clean and normalize data"""
    
    @staticmethod
    def clean_html(text: str) -> str:
        """Remove HTML tags"""
        if not isinstance(text, str):
            return ""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip()
    
    @staticmethod
    def normalize_genres(genres: Any) -> List[str]:
        """Normalize genres"""
        if isinstance(genres, list):
            return [g.lower().strip() for g in genres if g]
        if isinstance(genres, str):
            try:
                import ast
                parsed = ast.literal_eval(genres)
                if isinstance(parsed, list):
                    return [g.lower().strip() for g in parsed if g]
            except:
                return [g.strip().lower() for g in genres.split(',') if g.strip()]
        return []
    
    @staticmethod
    def clean_title(title: str) -> str:
        """Clean title"""
        if not isinstance(title, str):
            return ""
        # Remove year from title
        title = re.sub(r'\s*\(\d{4}\)\s*$', '', title)
        # Remove special characters
        title = re.sub(r'[^\w\s\-]', '', title)
        return title.strip()
    
    @staticmethod
    def clean_description(desc: str) -> str:
        """Clean description"""
        if not isinstance(desc, str):
            return ""
        desc = DataCleaner.clean_html(desc)
        desc = re.sub(r'\s+', ' ', desc)  # Remove extra spaces
        return desc.strip()
    
    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Clean entire DataFrame"""
        logger.info("Cleaning dataframe...")
        df = df.copy()
        
        # Clean text columns
        if 'title' in df.columns:
            df['title'] = df['title'].fillna('').astype(str)
            df['title'] = df['title'].apply(DataCleaner.clean_title)
        
        if 'description' in df.columns:
            df['description'] = df['description'].fillna('').astype(str)
            df['description'] = df['description'].apply(DataCleaner.clean_description)
        
        # Clean genres
        if 'genres' in df.columns:
            df['genres'] = df['genres'].apply(DataCleaner.normalize_genres)
        
        # Clean numeric columns
        if 'popularity' in df.columns:
            df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce').fillna(0)
        
        # Clean image URLs
        if 'image' in df.columns:
            df['image'] = df['image'].fillna('').astype(str)
        
        # Remove duplicates
        if 'id' in df.columns:
            df = df.drop_duplicates(subset=['id'])
        
        logger.info(f"Cleaned dataframe: {len(df)} rows")
        return df