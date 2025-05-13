from __future__ import annotations
from typing import TYPE_CHECKING
from cachetools import TTLCache
from project.settings import POSTS_RESPONSE_CACHE_SECONDS

if TYPE_CHECKING:
    from app.models import Post

# Cache for storing user posts with time-to-live expiration
cache: TTLCache[int, list[Post]] = TTLCache(maxsize=100, ttl=POSTS_RESPONSE_CACHE_SECONDS)


def get_cached_posts(user_id: int):
    """
    Retrieve cached posts for a specific user.
    
    Args:
        user_id (int): ID of the user whose posts to retrieve.
    
    Returns:
        list or None: List of cached posts if available, None otherwise.
    """
    return cache.get(user_id)


def set_cached_posts(user_id: int, posts:list[Post]):
    """
    Store posts in cache for a specific user.
    
    Args:
        user_id (int): ID of the user whose posts are being cached.
        posts (list): List of posts to cache.
    """
    cache[user_id] = posts

