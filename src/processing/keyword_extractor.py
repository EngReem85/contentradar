from typing import List, Dict, Any
from keybert import KeyBERT
import logging

logger = logging.getLogger(__name__)

class KeywordExtractor:
    """Extract keywords from text"""
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load KeyBERT model"""
        try:
            self.model = KeyBERT()
            logger.info("KeyBERT model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading KeyBERT: {e}")
            self.model = None
    
    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """Extract keywords from text"""
        if not text or self.model is None:
            return []
        
        try:
            keywords = self.model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words='english',
                top_n=top_n
            )
            return [kw[0] for kw in keywords]
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def extract_keywords_batch(self, texts: List[str], top_n: int = 5) -> List[List[str]]:
        """Extract keywords from multiple texts"""
        results = []
        for text in texts:
            keywords = self.extract_keywords(text, top_n)
            results.append(keywords)
        return results