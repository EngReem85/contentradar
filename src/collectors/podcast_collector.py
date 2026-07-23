from typing import List, Dict, Any, Optional
from .base_collector import BaseCollector
from src.utils.config import Config
import logging

logger = logging.getLogger(__name__)

class PodcastCollector(BaseCollector):
    """Collect data from ListenNotes"""
    
    BASE_URL = "https://listen-api.listennotes.com/api/v2/search"
    
    def __init__(self):
        super().__init__("podcast")
        self.api_key = Config.PODCAST_API_KEY
    
    def collect(self, query: str = "movies", 
                max_results: int = 50, **kwargs) -> List[Dict[str, Any]]:
        """Collect podcasts from ListenNotes"""
        
        if not self.api_key:
            logger.warning("PODCAST_API_KEY not found in .env")
            return []
        
        params = {
            "q": query,
            "type": "podcast",
            "len_min": 0,
            "len_max": 9999,
            "offset": 0,
            "only_in": "title,description",
            "sort_by_date": 0,
        }
        
        headers = {
            "X-ListenAPI-Key": self.api_key
        }
        
        try:
            response = self.session.get(self.BASE_URL, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("results", [])[:max_results]:
                image_url = item.get("image") or item.get("thumbnail") or ""
                
                results.append({
                    "id": f"pod_{item.get('id', '')}",
                    "title": item.get("title_original", ""),
                    "description": item.get("description_original", ""),
                    "genres": [],
                    "popularity": float(item.get("listennotes_editors_choice_score", 0) or 0),
                    "image": image_url,
                    "content_type": "podcast",
                    "source": "podcast",
                    "metadata": {
                        "podcast_id": item.get("id"),
                        "listen_score": item.get("listennotes_editors_choice_score", 0)
                    }
                })
            
            logger.info(f"Collected {len(results)} podcasts from ListenNotes")
            return results
            
        except Exception as e:
            logger.error(f"Error collecting from ListenNotes: {e}")
            return []