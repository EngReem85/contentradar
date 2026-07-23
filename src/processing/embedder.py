import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

from src.utils.config import Config

logger = logging.getLogger(__name__)

class Embedder:
    """Generate embeddings for content"""
    
    def __init__(self, model_name: str = "sentence-transformers/multi-qa-mpnet-base-dot-v1"):
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the embedding model"""
        if self.model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name, device="cpu")
    
    def generate(self, df: pd.DataFrame, 
                 text_column: str = "text_features",
                 save: bool = True) -> np.ndarray:
        """Generate embeddings for dataframe"""
        
        if text_column not in df.columns:
            logger.warning(f"Column '{text_column}' not found, creating text features")
            df["text_features"] = df.apply(self._create_text_features, axis=1)
        
        texts = df["text_features"].tolist()
        
        logger.info(f"Encoding {len(texts)} items...")
        embeddings = self.model.encode(
            texts, 
            batch_size=32, 
            show_progress_bar=True
        )
        
        if save:
            embed_path = Config.EMBEDDINGS_DIR / "embeddings.npy"
            embed_path.parent.mkdir(parents=True, exist_ok=True)
            np.save(embed_path, embeddings)
            logger.info(f"Saved embeddings to {embed_path}")
        
        return embeddings
    
    def _create_text_features(self, row: pd.Series) -> str:
        """Create combined text features"""
        title = str(row.get("title", ""))
        description = str(row.get("description", ""))
        genres = " ".join(row.get("genres", [])) if isinstance(row.get("genres"), list) else ""
        content_type = str(row.get("content_type", ""))
        source = str(row.get("source", ""))
        
        return f"{title}. {description}. Genres: {genres}. Type: {content_type}. Source: {source}"
    
    def encode(self, text: str) -> np.ndarray:
        """Encode single text"""
        self._load_model()
        return self.model.encode(text)
    
    def load_embeddings(self, path: Optional[Path] = None) -> Optional[np.ndarray]:
        """Load saved embeddings"""
        if path is None:
            path = Config.EMBEDDINGS_DIR / "embeddings.npy"
        
        if path.exists():
            logger.info(f"Loading embeddings from {path}")
            return np.load(path)
        
        logger.warning(f"Embeddings file not found: {path}")
        return None