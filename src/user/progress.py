from datetime import datetime
from typing import Dict, Any, Optional
from src.user.manager import UserManager
import logging

logger = logging.getLogger(__name__)

class ProgressTracker:
    """Track user progress"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
    
    def update_progress(self, item_id: str, 
                        progress: int = 10, 
                        completed: bool = False) -> bool:
        """Update progress for an item"""
        try:
            progress_data = self.user_manager.get_progress()
            
            if item_id not in progress_data:
                progress_data[item_id] = {
                    "progress": 0,
                    "completed": False,
                    "started": datetime.now().isoformat()
                }
            
            # Update progress
            if not progress_data[item_id]['completed']:
                progress_data[item_id]['progress'] = min(100, progress)
                progress_data[item_id]['completed'] = completed
                progress_data[item_id]['updated'] = datetime.now().isoformat()
                
                if completed:
                    progress_data[item_id]['completed_at'] = datetime.now().isoformat()
            
            self.user_manager._save_json(
                self.user_manager.progress_file,
                progress_data
            )
            
            logger.info(f"Updated progress for item {item_id}: {progress}%")
            return True
            
        except Exception as e:
            logger.error(f"Error updating progress: {e}")
            return False
    
    def get_progress(self, item_id: str) -> Optional[Dict]:
        """Get progress for an item"""
        progress_data = self.user_manager.get_progress()
        return progress_data.get(item_id)
    
    def get_completion_rate(self) -> float:
        """Get overall completion rate"""
        progress_data = self.user_manager.get_progress()
        
        if not progress_data:
            return 0.0
        
        completed = sum(1 for p in progress_data.values() if p.get('completed', False))
        return (completed / len(progress_data)) * 100 if progress_data else 0