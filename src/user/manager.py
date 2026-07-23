import json
from pathlib import Path
from typing import Dict, Any, Optional
from src.utils.config import Config
import logging

logger = logging.getLogger(__name__)

class UserManager:
    """Manage user data"""
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.user_dir = Config.USERS_DIR / user_id
        self.user_dir.mkdir(parents=True, exist_ok=True)
        
        self.ratings_file = self.user_dir / "ratings.json"
        self.watchlist_file = self.user_dir / "watchlist.json"
        self.progress_file = self.user_dir / "progress.json"
        self.preferences_file = self.user_dir / "preferences.json"
        
        self._ensure_files()
    
    def _ensure_files(self):
        """Ensure all required files exist"""
        for file in [self.ratings_file, self.watchlist_file, 
                    self.progress_file, self.preferences_file]:
            if not file.exists():
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump({}, f)
    
    def _load_json(self, filepath: Path) -> Dict:
        """Load JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_json(self, filepath: Path, data: Dict):
        """Save JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_ratings(self) -> Dict:
        """Get user ratings"""
        return self._load_json(self.ratings_file)
    
    def get_watchlist(self) -> Dict:
        """Get user watchlist"""
        return self._load_json(self.watchlist_file)
    
    def get_progress(self) -> Dict:
        """Get user progress"""
        return self._load_json(self.progress_file)
    
    def get_preferences(self) -> Dict:
        """Get user preferences"""
        return self._load_json(self.preferences_file)