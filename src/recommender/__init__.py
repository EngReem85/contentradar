"""
Recommender system module
"""

from .base import BaseRecommender
from .hybrid import HybridRecommender
from .fast import FastRecommender
from .filters import FilterEngine
from .mmr import mmr_rerank

__all__ = [
    'BaseRecommender',
    'HybridRecommender',
    'FastRecommender',
    'FilterEngine',
    'mmr_rerank'
]