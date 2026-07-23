#!/usr/bin/env python
"""
Process and clean collected data
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.processing.cleaner import DataCleaner
from src.processing.normalizer import DataNormalizer
from src.utils.config import Config
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_data():
    """Process and clean data"""
    logger.info("Starting data processing...")
    
    Config.ensure_dirs()
    
    # Load raw data
    raw_path = Config.RAW_DIR / "content_raw.csv"
    if not raw_path.exists():
        logger.error(f"Raw data not found: {raw_path}")
        return None
    
    df = pd.read_csv(raw_path, encoding='utf-8')
    logger.info(f"Loaded {len(df)} raw items")
    
    # Clean
    cleaner = DataCleaner()
    df = cleaner.clean_dataframe(df)
    logger.info(f"After cleaning: {len(df)} items")
    
    # Normalize
    normalizer = DataNormalizer()
    df = normalizer.normalize_dataframe(df)
    
    # Save processed
    processed_path = Config.PROCESSED_DIR / "content.csv"
    df.to_csv(processed_path, index=False, encoding='utf-8')
    
    logger.info(f"Saved {len(df)} processed items to {processed_path}")
    return df

if __name__ == "__main__":
    process_data()