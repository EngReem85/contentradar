import pytest
import numpy as np
import pandas as pd
from src.recommender.hybrid import HybridRecommender
from src.recommender.mmr import mmr_rerank

def test_mmr_rerank():
    query_vec = np.array([1, 0])
    doc_vecs = np.array([
        [1, 0],  # Similar to query
        [0, 1],  # Different
        [1, 0.5] # Similar
    ])
    base_indices = [0, 1, 2]
    
    result = mmr_rerank(query_vec, doc_vecs, base_indices, top_k=2)
    
    assert len(result) == 2
    # Should pick the most relevant and diverse
    assert result[0] == 0
    assert result[1] in [1, 2]

def test_hybrid_recommender():
    df = pd.DataFrame({
        'id': ['1', '2'],
        'title': ['Test1', 'Test2'],
        'popularity': [10, 5],
        'content_type': ['movie', 'series']
    })
    embeddings = np.array([[1, 0], [0, 1]])
    
    recommender = HybridRecommender(df, embeddings)
    assert recommender.df is not None
    assert recommender.embeddings is not None