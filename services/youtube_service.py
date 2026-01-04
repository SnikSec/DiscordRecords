"""
YouTube Service
Handles YouTube search and video retrieval
"""
import yt_dlp
from typing import Optional


class YouTubeService:
    """Service for interacting with YouTube"""
    
    def __init__(self):
        """Initialize YouTube service"""
        self.ytdl_options = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'extract_flat': True  # Don't download, just get info
        }
    
    async def search(self, query: str, limit: int = 1) -> Optional[str]:
        """
        Search YouTube for a video
        
        Args:
            query: Search query
            limit: Number of results to return (default 1)
            
        Returns:
            Video URL or None if not found
        """
        try:
            with yt_dlp.YoutubeDL(self.ytdl_options) as ytdl:
                # Search YouTube
                search_query = f"ytsearch{limit}:{query}"
                info = ytdl.extract_info(search_query, download=False)
                
                if 'entries' in info and info['entries']:
                    # Return the first result URL
                    video = info['entries'][0]
                    return f"https://www.youtube.com/watch?v={video['id']}"
                
                return None
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return None
    
    async def get_video_info(self, url: str) -> Optional[dict]:
        """
        Get information about a YouTube video
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary with video information or None if error
        """
        try:
            ytdl_options = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ytdl_options) as ytdl:
                info = ytdl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'url': info.get('url', ''),
                    'webpage_url': info.get('webpage_url', url),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0)
                }
        except Exception as e:
            print(f"Error getting YouTube video info: {e}")
            return None
    
    async def search_playlist(self, query: str) -> Optional[str]:
        """
        Search for a YouTube playlist
        
        Args:
            query: Search query for playlist
            
        Returns:
            Playlist URL or None if not found
        """
        try:
            with yt_dlp.YoutubeDL(self.ytdl_options) as ytdl:
                # Search for playlists
                search_query = f"ytsearch1:playlist {query}"
                info = ytdl.extract_info(search_query, download=False)
                
                if 'entries' in info and info['entries']:
                    entry = info['entries'][0]
                    # Check if it's a playlist
                    if 'playlist' in entry.get('url', ''):
                        return entry['url']
                
                return None
        except Exception as e:
            print(f"Error searching YouTube playlist: {e}")
            return None
