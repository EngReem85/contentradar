from datetime import datetime
from typing import Dict, Any, Optional
from src.user.manager import UserManager
import logging

logger = logging.getLogger(__name__)

class WatchlistManager:
    """Manage user watchlist"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
    
    def add_to_watchlist(self, item_id: str, notes: str = "", 
                         status: str = "plan_to_watch") -> bool:
        """Add item to watchlist"""
        try:
            watchlist = self.user_manager.get_watchlist()
            
            watchlist[item_id] = {
                "added": datetime.now().isoformat(),
                "notes": notes,
                "status": status,  # plan_to_watch, watching, completed, on_hold
                "updated": datetime.now().isoformat()
            }
            
            self.user_manager._save_json(
                self.user_manager.watchlist_file,
                watchlist
            )
            
            logger.info(f"Added item {item_id} to watchlist")
            return True
            
        except Exception as e:
            logger.error(f"Error adding to watchlist: {e}")
            return False
    
    def update_status(self, item_id: str, status: str) -> bool:
        """Update watchlist status"""
        try:
            watchlist = self.user_manager.get_watchlist()
            
            if item_id in watchlist:
                watchlist[item_id]['status'] = status
                watchlist[item_id]['updated'] = datetime.now().isoformat()
                
                self.user_manager._save_json(
                    self.user_manager.watchlist_file,
                    watchlist
                )
                
                logger.info(f"Updated status for item {item_id} to {status}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating watchlist status: {e}")
            return False
    
    def remove_from_watchlist(self, item_id: str) -> bool:
        """Remove item from watchlist"""
        try:
            watchlist = self.user_manager.get_watchlist()
            
            if item_id in watchlist:
                del watchlist[item_id]
                
                self.user_manager._save_json(
                    self.user_manager.watchlist_file,
                    watchlist
                )
                
                logger.info(f"Removed item {item_id} from watchlist")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error removing from watchlist: {e}")
            return False