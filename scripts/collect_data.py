#!/usr/bin/env python
"""
Collect data from all sources
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.collectors import TMDBCollector, YouTubeCollector, PodcastCollector, AniListCollector
from src.utils.config import Config
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def collect_all():
    """Collect data from all sources"""
    logger.info("Starting data collection...")
    
    Config.ensure_dirs()
    
    all_items = []
    
    # TMDB
    logger.info("Collecting from TMDB...")
    tmdb = TMDBCollector()
    movies = tmdb.collect(content_type="movie", pages=2)
    series = tmdb.collect(content_type="tv", pages=2)
    all_items.extend(movies)
    all_items.extend(series)
    logger.info(f"Collected {len(movies)} movies and {len(series)} series")
    
    # YouTube
    logger.info("Collecting from YouTube...")
    youtube = YouTubeCollector()
    videos = youtube.collect(query="movie trailers", max_results=10)
    all_items.extend(videos)
    logger.info(f"Collected {len(videos)} videos")
    
    # Podcasts
    logger.info("Collecting from podcasts...")
    podcast = PodcastCollector()
    podcasts = podcast.collect(query="movies", max_results=10)
    all_items.extend(podcasts)
    logger.info(f"Collected {len(podcasts)} podcasts")
    
    # AniList
    logger.info("Collecting from AniList...")
    anilist = AniListCollector()
    anime = anilist.collect(query="anime", per_page=10)
    all_items.extend(anime)
    logger.info(f"Collected {len(anime)} anime")
    
    # Save
    if all_items:
        df = pd.DataFrame(all_items)
        
        # Remove duplicates
        if 'id' in df.columns:
            df = df.drop_duplicates(subset=['id'])
        
        # Ensure directories exist
        Config.RAW_DIR.mkdir(parents=True, exist_ok=True)
        raw_path = Config.RAW_DIR / "content_raw.csv"
        df.to_csv(raw_path, index=False, encoding='utf-8')
        
        logger.info(f"? Saved {len(df)} items to {raw_path}")
        return df
    else:
        logger.warning("?? No items collected!")
        return None

if __name__ == "__main__":
    collect_all()