from typing import List, Dict, Any, Optional
from .base_collector import BaseCollector
from src.utils.config import Config
import logging

logger = logging.getLogger(__name__)

class YouTubeCollector(BaseCollector):
    """Collect data from YouTube"""
    
    SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
    VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
    
    def __init__(self):
        super().__init__("youtube")
        self.api_key = Config.YOUTUBE_API_KEY
    
    def collect(self, query: str = "movie trailers", 
                max_results: int = 50, **kwargs) -> List[Dict[str, Any]]:
        """Collect videos from YouTube"""
        
        if not self.api_key:
            logger.warning("YOUTUBE_API_KEY not found in .env")
            return []
        
        params = {
            "part": "snippet",
            "q": query,
            "key": self.api_key,
            "maxResults": min(max_results, 50),
            "type": "video",
            "safeSearch": "none",
        }
        
        try:
            data = self._make_request(self.SEARCH_URL, params=params)
            results = []
            
            for item in data.get("items", []):
                snippet = item["snippet"]
                thumb = snippet.get("thumbnails", {}).get("high") or \
                       snippet.get("thumbnails", {}).get("default") or {}
                image_url = thumb.get("url", "")
                
                results.append({
                    "id": f"yt_{item['id']['videoId']}",
                    "title": snippet.get("title", ""),
                    "description": snippet.get("description", ""),
                    "genres": [],
                    "popularity": 0.0,
                    "image": image_url,
                    "content_type": "youtube",
                    "source": "youtube",
                    "metadata": {
                        "video_id": item["id"]["videoId"],
                        "channel": snippet.get("channelTitle", ""),
                        "published_at": snippet.get("publishedAt", "")
                    }
                })
            
            logger.info(f"Collected {len(results)} videos from YouTube")
            return results
            
        except Exception as e:
            logger.error(f"Error collecting from YouTube: {e}")
            return []