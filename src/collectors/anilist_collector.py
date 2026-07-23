import sys
from pathlib import Path

# ÅÖÇÝÉ ãÌáÏ src Åáì ãÓÇÑ Python
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.config import Config
from .base_collector import BaseCollector
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AniListCollector(BaseCollector):
    """Collect data from AniList"""
    
    GRAPHQL_URL = "https://graphql.anilist.co"
    
    def __init__(self):
        super().__init__("anilist")
        self.api_key = Config.ANILIST_API_KEY
    
    def collect(self, query: str = "anime", 
                page: int = 1, per_page: int = 50, **kwargs) -> List[Dict[str, Any]]:
        """Collect anime from AniList"""
        
        graphql_query = """
        query ($search: String, $page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
                media(search: $search, type: ANIME, sort: POPULARITY_DESC) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    description
                    genres
                    popularity
                    coverImage {
                        large
                        medium
                    }
                    averageScore
                    episodes
                    status
                    startDate {
                        year
                        month
                        day
                    }
                }
            }
        }
        """
        
        variables = {
            "search": query,
            "page": page,
            "perPage": min(per_page, 50)
        }
        
        try:
            response = self.session.post(
                self.GRAPHQL_URL,
                json={"query": graphql_query, "variables": variables},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("data", {}).get("Page", {}).get("media", []):
                title = item.get("title", {})
                title_str = title.get("english") or title.get("romaji") or title.get("native", "")
                
                cover = item.get("coverImage", {})
                image_url = cover.get("large") or cover.get("medium", "")
                
                results.append({
                    "id": f"ani_{item.get('id')}",
                    "title": title_str,
                    "description": item.get("description", "").replace("<br>", ""),
                    "genres": item.get("genres", []),
                    "popularity": float(item.get("popularity", 0)),
                    "image": image_url,
                    "content_type": "anime",
                    "source": "anilist",
                    "metadata": {
                        "anilist_id": item.get("id"),
                        "average_score": item.get("averageScore", 0),
                        "episodes": item.get("episodes", 0),
                        "status": item.get("status", ""),
                        "start_year": item.get("startDate", {}).get("year")
                    }
                })
            
            logger.info(f"Collected {len(results)} anime from AniList")
            return results
            
        except Exception as e:
            logger.error(f"Error collecting from AniList: {e}")
            return []