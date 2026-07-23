"""
User management module
"""

from .manager import UserManager
from .ratings import RatingsManager
from .watchlist import WatchlistManager
from .progress import ProgressTracker

__all__ = [
    'UserManager',
    'RatingsManager', 
    'WatchlistManager',
    'ProgressTracker'
]