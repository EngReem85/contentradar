import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Optional

from src.utils.config import Config
from src.recommender.base import BaseRecommender
from src.recommender.mmr import mmr_rerank
import logging

logger = logging.getLogger(__name__)

class HybridRecommender(BaseRecommender):
    """Hybrid recommendation system combining text similarity and popularity"""
    
    def recommend(self, query: str, embedder_model, 
                  top_k: int = None, 
                  content_types: List[str] = None, 
                  use_mmr: bool = True) -> List[Dict[str, Any]]:
        """Search and recommend based on text query"""
        
        if top_k is None:
            top_k = Config.DEFAULT_TOP_K
        
        logger.info(f"Generating recommendations for query: '{query}'")
        
        # Filter by content type
        df_filtered = self.df
        embeddings_filtered = self.embeddings
        
        if content_types:
            mask = self.df['content_type'].isin(content_types)
            df_filtered = self.df[mask]
            embeddings_filtered = self.embeddings[mask]
        
        if len(df_filtered) == 0:
            logger.warning("No items found matching content types")
            return []
        
        # Generate query embedding
        query_emb = embedder_model.encode(query).reshape(1, -1)
        
        # Calculate similarity
        text_sim = cosine_similarity(query_emb, embeddings_filtered)[0]
        
        # Add popularity factor
        pop = df_filtered['popularity'].fillna(0).values
        pop_norm = self._normalize(pop)
        
        # Hybrid score
        hybrid_score = (
            Config.TEXT_WEIGHT * text_sim +
            Config.POPULARITY_WEIGHT * pop_norm
        )
        
        # Select top candidates
        base_indices = np.argsort(hybrid_score)[::-1][:top_k * 3]
        
        # Apply MMR for diversity
        if use_mmr:
            final_indices = mmr_rerank(
                query_vec=query_emb[0],
                doc_vecs=embeddings_filtered,
                base_indices=base_indices,
                top_k=top_k,
                lambda_param=Config.MMR_LAMBDA
            )
        else:
            final_indices = base_indices[:top_k]
        
        # Prepare results
        results = df_filtered.iloc[final_indices].copy()
        results['similarity'] = hybrid_score[final_indices]
        
        logger.info(f"Returning {len(results)} recommendations")
        return results.to_dict(orient='records')
    
    def similar_items(self, item_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Find similar items to a given item"""
        
        logger.info(f"Finding similar items for: {item_id}")
        
        # Find item index
        idx_list = self.df.index[self.df['id'] == item_id].tolist()
        if not idx_list:
            logger.warning(f"Item not found: {item_id}")
            return []
        
        idx = idx_list[0]
        
        # Calculate similarity
        target_emb = self.embeddings[idx].reshape(1, -1)
        similarities = cosine_similarity(target_emb, self.embeddings)[0]
        
        # Exclude the item itself
        similarities[idx] = -1
        
        # Get top similar items
        similar_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = self.df.iloc[similar_indices].copy()
        results['similarity'] = similarities[similar_indices]
        
        logger.info(f"Found {len(results)} similar items")
        return results.to_dict(orient='records')