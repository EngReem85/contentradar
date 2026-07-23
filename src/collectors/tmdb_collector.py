from typing import List, Dict, Any, Optional
from src.utils.config import Config
from src.collectors.base_collector import BaseCollector
import logging

logger = logging.getLogger(__name__)

class TMDBCollector(BaseCollector):
    """Collect data from TMDB"""
    
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
    
    def __init__(self):
        super().__init__("tmdb")
        self.api_key = Config.TMDB_API_KEY
    
    def collect(self, query: Optional[str] = None, 
                content_type: str = "movie", 
                pages: int = 2, **kwargs) -> List[Dict[str, Any]]:
        """Collect movies/series from TMDB"""
        
        if not self.api_key:
            logger.warning("TMDB_API_KEY not found in .env")
            return []
        
        if query:
            endpoint = f"/search/{content_type}"
        else:
            endpoint = f"/discover/{content_type}"
        
        results = []
        for page in range(1, pages + 1):
            params = {
                "api_key": self.api_key,
                "page": page,
                "language": "en-US"
            }
            if query:
                params["query"] = query
            
            try:
                data = self._make_request(
                    f"{self.BASE_URL}{endpoint}", 
                    params=params
                )
                
                for item in data.get("results", []):
                    normalized = self.normalize_tmdb_item(item, content_type)
                    results.append(normalized)
                    
                logger.info(f"Collected page {page} from TMDB")
                    
            except Exception as e:
                logger.error(f"Error collecting page {page}: {e}")
                continue
        
        logger.info(f"Total collected from TMDB: {len(results)} items")
        return results
    
    def normalize_tmdb_item(self, item: Dict, content_type: str) -> Dict:
        """Normalize TMDB item"""
        image_path = item.get("poster_path") or item.get("backdrop_path")
        image_url = f"{self.IMAGE_BASE}{image_path}" if image_path else ""
        
        return {
            "id": f"tmdb_{item.get('id')}",
            "title": item.get("title") or item.get("name", ""),
            "description": item.get("overview", ""),
            "genres": [],
            "popularity": float(item.get("popularity", 0)),
            "image": image_url,
            "content_type": content_type,
            "source": "tmdb",
            "metadata": {
                "tmdb_id": item.get("id"),
                "vote_average": item.get("vote_average", 0),
                "vote_count": item.get("vote_count", 0),
                "release_date": item.get("release_date") or item.get("first_air_date"),
                "original_language": item.get("original_language")
            }
        }