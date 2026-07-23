from datetime import datetime
from typing import Dict, Any, Optional
from src.user.manager import UserManager
import logging

logger = logging.getLogger(__name__)

class RatingsManager:
    """Manage user ratings"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
    
    def add_rating(self, item_id: str, rating: float, review: str = "") -> bool:
        """Add a rating for an item"""
        try:
            ratings = self.user_manager.get_ratings()
            
            ratings[item_id] = {
                "rating": float(rating),
                "review": review,
                "timestamp": datetime.now().isoformat(),
                "updated": True
            }
            
            self.user_manager._save_json(
                self.user_manager.ratings_file, 
                ratings
            )
            
            logger.info(f"Added rating {rating} for item {item_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding rating: {e}")
            return False
    
    def get_rating(self, item_id: str) -> Optional[Dict]:
        """Get rating for an item"""
        ratings = self.user_manager.get_ratings()
        return ratings.get(item_id)
    
    def get_average_rating(self) -> float:
        """Get average rating"""
        ratings = self.user_manager.get_ratings()
        if not ratings:
            return 0.0
        
        total = sum(r['rating'] for r in ratings.values())
        return total / len(ratings)
    
    def delete_rating(self, item_id: str) -> bool:
        """Delete a rating"""
        try:
            ratings = self.user_manager.get_ratings()
            if item_id in ratings:
                del ratings[item_id]
                self.user_manager._save_json(
                    self.user_manager.ratings_file,
                    ratings
                )
                logger.info(f"Deleted rating for item {item_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting rating: {e}")
            return False