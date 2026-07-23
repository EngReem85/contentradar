import numpy as np
import faiss
from typing import List, Dict, Any, Optional
from src.recommender.base import BaseRecommender
import logging

logger = logging.getLogger(__name__)

class FastRecommender(BaseRecommender):
    """Fast recommendation using FAISS"""
    
    def __init__(self, df, embeddings):
        super().__init__(df, embeddings)
        self.index = None
        self._build_index()
    
    def _build_index(self):
        """Build FAISS index"""
        logger.info("Building FAISS index...")
        
        # Normalize embeddings
        embeddings_norm = self.embeddings.astype(np.float32)
        
        # Create index
        dimension = embeddings_norm.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings_norm)
        
        logger.info(f"FAISS index built with {self.index.ntotal} items")
    
    def recommend(self, query_vec: np.ndarray, 
                  top_k: int = 10, 
                  content_types: List[str] = None) -> List[Dict[str, Any]]:
        """Fast recommendation using FAISS"""
        
        if self.index is None:
            logger.error("FAISS index not built")
            return []
        
        # Normalize query
        query_vec = query_vec.astype(np.float32).reshape(1, -1)
        
        # Search
        distances, indices = self.index.search(query_vec, min(top_k * 2, self.index.ntotal))
        
        # Get results
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.df):
                item = self.df.iloc[idx].to_dict()
                
                # Apply content type filter
                if content_types and item.get('content_type') not in content_types:
                    continue
                
                item['similarity'] = float(dist)
                results.append(item)
                
                if len(results) >= top_k:
                    break
        
        return results