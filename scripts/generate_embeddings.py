#!/usr/bin/env python
"""
Generate embeddings for content
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.processing.embedder import Embedder
from src.utils.config import Config
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_embeddings():
    """Generate embeddings"""
    logger.info("Starting embedding generation...")
    
    Config.ensure_dirs()
    
    # Load processed data
    processed_path = Config.PROCESSED_DIR / "content.csv"
    if not processed_path.exists():
        logger.error(f"Processed data not found: {processed_path}")
        return None
    
    df = pd.read_csv(processed_path, encoding='utf-8')
    logger.info(f"Loaded {len(df)} processed items")
    
    # Generate embeddings
    embedder = Embedder()
    embeddings = embedder.generate(df, save=True)
    
    logger.info(f"Generated embeddings: {embeddings.shape}")
    return embeddings

if __name__ == "__main__":
    generate_embeddings()