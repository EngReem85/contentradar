from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseCollector(ABC):
    """Base class for data collectors"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ContentRadar/2.0'
        })
    
    @abstractmethod
    def collect(self, **kwargs) -> List[Dict[str, Any]]:
        """Collect content from source"""
        pass
    
    @retry(stop=stop_after_attempt(3), 
           wait=wait_exponential(multiplier=1, min=2, max=10))
    def _make_request(self, url: str, params: Optional[Dict] = None) -> Dict:
        """Make request with retry"""
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def normalize_item(self, item: Dict) -> Dict:
        """Normalize item data"""
        return {
            "id": str(item.get("id", "")),
            "title": str(item.get("title", "")),
            "description": str(item.get("description", "")),
            "genres": item.get("genres", []),
            "popularity": float(item.get("popularity", 0)),
            "image": str(item.get("image", "")),
            "content_type": str(item.get("content_type", "")),
            "source": self.source_name,
            "metadata": item.get("metadata", {})
        }