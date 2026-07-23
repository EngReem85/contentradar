"""
Data collectors module
"""

from src.collectors.base_collector import BaseCollector
from src.collectors.tmdb_collector import TMDBCollector
from src.collectors.youtube_collector import YouTubeCollector
from src.collectors.podcast_collector import PodcastCollector
from src.collectors.anilist_collector import AniListCollector

__all__ = [
    'BaseCollector',
    'TMDBCollector',
    'YouTubeCollector',
    'PodcastCollector',
    'AniListCollector'
]