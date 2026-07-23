import json
from datetime import datetime, timedelta
from typing import Any, Optional
from pathlib import Path
import hashlib
import logging

# ✅ التصحيح: استيراد Config من المسار الصحيح
from src.utils.config import Config

logger = logging.getLogger(__name__)

class CacheManager:
    """Cache management system"""
    
    def __init__(self):
        self.cache_dir = Config.CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory_cache = {}
        self.ttl = Config.CACHE_TTL
        self.max_size = Config.CACHE_MAX_SIZE
    
    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path"""
        hashed = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hashed}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve from cache"""
        # Check memory first
        if key in self.memory_cache:
            data, timestamp = self.memory_cache[key]
            if (datetime.now() - timestamp).seconds < self.ttl:
                logger.debug(f"Cache hit (memory): {key}")
                return data
            else:
                del self.memory_cache[key]
        
        # Check file cache
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cache_time = datetime.fromisoformat(data['timestamp'])
                    if cache_time + timedelta(seconds=self.ttl) > datetime.now():
                        value = data['value']
                        self.memory_cache[key] = (value, datetime.now())
                        logger.debug(f"Cache hit (file): {key}")
                        return value
                    else:
                        cache_path.unlink()
                        logger.debug(f"Cache expired: {key}")
            except Exception as e:
                logger.error(f"Error reading cache {key}: {e}")
        
        return None
    
    def set(self, key: str, value: Any):
        """Save to cache"""
        if len(self.memory_cache) >= self.max_size:
            oldest = min(self.memory_cache.keys(), 
                        key=lambda k: self.memory_cache[k][1])
            del self.memory_cache[oldest]
        
        self.memory_cache[key] = (value, datetime.now())
        
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'key': key,
                    'value': value,
                    'timestamp': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            logger.debug(f"Cache saved: {key}")
        except Exception as e:
            logger.error(f"Error saving cache {key}: {e}")
    
    def clear(self):
        """Clear all cache"""
        self.memory_cache.clear()
        for file in self.cache_dir.glob('*.json'):
            try:
                file.unlink()
                logger.debug(f"Deleted cache file: {file}")
            except Exception as e:
                logger.error(f"Error deleting cache {file}: {e}")
        logger.info("Cache cleared")

# Global cache instance
cache = CacheManager()