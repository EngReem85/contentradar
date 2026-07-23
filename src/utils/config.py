import os
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class Config:
    """Application Configuration"""
    
    # API Keys
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    PODCAST_API_KEY = os.getenv("LISTENNOTES_API_KEY")
    ANILIST_API_KEY = os.getenv("ANILIST_API_KEY")
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    RAW_DIR = DATA_DIR / "raw"
    PROCESSED_DIR = DATA_DIR / "processed"
    CACHE_DIR = DATA_DIR / "cache"
    USERS_DIR = DATA_DIR / "users"
    EMBEDDINGS_DIR = DATA_DIR / "embeddings"
    SKILLS_DIR = DATA_DIR / "skills"
    
    # App
    APP_NAME = "ContentRadar"
    VERSION = "2.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Recommendation
    DEFAULT_TOP_K = 20
    TEXT_WEIGHT = 0.55
    POPULARITY_WEIGHT = 0.25
    GENRE_WEIGHT = 0.20
    MMR_LAMBDA = 0.7
    
    # Cache
    CACHE_TTL = 3600  # seconds
    CACHE_MAX_SIZE = 1000
    
    @classmethod
    def ensure_dirs(cls):
        """Create necessary directories"""
        for path in [
            cls.RAW_DIR, cls.PROCESSED_DIR, cls.CACHE_DIR,
            cls.USERS_DIR, cls.EMBEDDINGS_DIR, cls.SKILLS_DIR
        ]:
            try:
                path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Directory ensured: {path}")
            except Exception as e:
                logger.error(f"Error creating directory {path}: {e}")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        required_keys = ['TMDB_API_KEY']
        missing = [key for key in required_keys if not getattr(cls, key)]
        
        if missing:
            logger.warning(f"Missing environment variables: {missing}")
            return False
        
        return True