from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class BaseRecommender(ABC):
    """Base class for recommenders"""
    
    def __init__(self, df: pd.DataFrame, embeddings: np.ndarray):
        self.df = df
        self.embeddings = embeddings
        self._validate_data()
    
    def _validate_data(self):
        """Validate input data"""
        if self.df is None or len(self.df) == 0:
            raise ValueError("DataFrame is empty")
        
        if self.embeddings is None or len(self.embeddings) == 0:
            raise ValueError("Embeddings are empty")
        
        if len(self.df) != len(self.embeddings):
            raise ValueError(f"DataFrame length ({len(self.df)}) does not match embeddings length ({len(self.embeddings)})")
    
    @abstractmethod
    def recommend(self, **kwargs) -> List[Dict[str, Any]]:
        """Generate recommendations"""
        pass
    
    @staticmethod
    def _normalize(x: np.ndarray) -> np.ndarray:
        """Normalize values to 0-1"""
        x = np.array(x, dtype=float)
        if x.max() - x.min() < 1e-9:
            return np.zeros_like(x)
        return (x - x.min()) / (x.max() - x.min())
    
    def _get_item_by_id(self, item_id: str) -> Optional[Dict]:
        """Get item by ID"""
        try:
            idx = self.df.index[self.df['id'] == item_id].tolist()
            if idx:
                return self.df.iloc[idx[0]].to_dict()
            return None
        except:
            return None