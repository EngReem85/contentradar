import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
import logging

logger = logging.getLogger(__name__)

def mmr_rerank(query_vec: np.ndarray, 
               doc_vecs: np.ndarray, 
               base_indices: List[int], 
               top_k: int = 10, 
               lambda_param: float = 0.7) -> List[int]:
    """
    Maximum Marginal Relevance reranking
    Balances relevance and diversity
    
    Args:
        query_vec: Query embedding
        doc_vecs: Document embeddings
        base_indices: Candidate indices
        top_k: Number of results to return
        lambda_param: Trade-off parameter (0 = diversity, 1 = relevance)
    
    Returns:
        List of selected indices
    """
    
    if not base_indices:
        return []
    
    selected = []
    candidates = list(base_indices)
    
    for _ in range(min(top_k, len(candidates))):
        best_i = None
        best_score = -1e9
        
        for i in candidates:
            # Relevance
            relevance = cosine_similarity(
                query_vec.reshape(1, -1),
                doc_vecs[i].reshape(1, -1)
            )[0][0]
            
            # Diversity (maximum similarity to selected)
            diversity = 0.0
            if selected:
                diversity = max([
                    cosine_similarity(
                        doc_vecs[i].reshape(1, -1),
                        doc_vecs[j].reshape(1, -1)
                    )[0][0]
                    for j in selected
                ])
            
            # MMR score
            mmr_score = lambda_param * relevance - (1 - lambda_param) * diversity
            
            if mmr_score > best_score:
                best_score = mmr_score
                best_i = i
        
        if best_i is not None:
            selected.append(best_i)
            candidates.remove(best_i)
    
    logger.info(f"MMR reranking completed: {len(selected)} items selected")
    return selected