"""Utility functions for the bot"""
import re
from typing import Optional


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to MM:SS format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string like "3:45"
    """
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def is_url(text: str) -> bool:
    """
    Check if text is a URL
    
    Args:
        text: Text to check
        
    Returns:
        True if text appears to be a URL
    """
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return bool(url_pattern.match(text))


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from URL
    
    Args:
        url: YouTube URL
        
    Returns:
        Video ID or None if not found
    """
    patterns = [
        r'(?:v=|/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def extract_playlist_id(url: str) -> Optional[str]:
    """
    Extract Spotify or YouTube playlist ID from URL
    
    Args:
        url: Playlist URL
        
    Returns:
        Playlist ID or None if not found
    """
    # Spotify playlist
    spotify_match = re.search(r'playlist/([a-zA-Z0-9]+)', url)
    if spotify_match:
        return spotify_match.group(1)
    
    # YouTube playlist
    youtube_match = re.search(r'[?&]list=([a-zA-Z0-9_-]+)', url)
    if youtube_match:
        return youtube_match.group(1)
    
    return None


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to max length with ellipsis
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
