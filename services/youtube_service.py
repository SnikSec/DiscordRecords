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
            'extract_flat': True,  # Don't download, just get info
            'nocheckcertificate': True,
            'remote_components': 'ejs:github',
        }
    
    def _is_valid_video_id(self, video_id: str) -> bool:
        """Check if a YouTube ID is a valid video ID (not a channel/playlist)"""
        if not video_id:
            return False
        if video_id.startswith(('UC', 'PL', 'VL', 'RD', 'FL', 'UU')):
            return False
        return True
    
    async def search(self, query: str, limit: int = 5, music_only: bool = True) -> Optional[str]:
        """
        Search YouTube for a video
        
        Args:
            query: Search query
            limit: Number of results to fetch (picks first valid one)
            music_only: If True, bias search toward music content
            
        Returns:
            Video URL or None if not found
        """
        try:
            with yt_dlp.YoutubeDL(self.ytdl_options) as ytdl:
                # Search with music-biased terms first
                if music_only:
                    search_query = f"ytsearch{limit}:{query} official audio"
                    try:
                        info = ytdl.extract_info(search_query, download=False)
                        if 'entries' in info and info['entries']:
                            for video in info['entries']:
                                if video and video.get('id') and self._is_valid_video_id(video['id']):
                                    return f"https://www.youtube.com/watch?v={video['id']}"
                    except Exception as e:
                        print(f"Music search failed for '{query}': {e}")
                
                # Fallback to regular YouTube search
                search_query = f"ytsearch{limit}:{query}"
                info = ytdl.extract_info(search_query, download=False)
                
                if 'entries' in info and info['entries']:
                    for video in info['entries']:
                        if video and video.get('id') and self._is_valid_video_id(video['id']):
                            return f"https://www.youtube.com/watch?v={video['id']}"
                
                print(f"No results found for: {query}")
                return None
        except Exception as e:
            print(f"Error searching YouTube for '{query}': {e}")
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
                'nocheckcertificate': True,
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

    async def search_playlist(self, query: str, limit: int = 20) -> Optional[list]:
        """
        Search YouTube for a playlist and return its video URLs.

        Args:
            query: Search query for playlist
            limit: Max number of tracks to return

        Returns:
            List of video URLs or None if not found
        """
        try:
            ytdl_options = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'default_search': 'ytsearch',
            }

            with yt_dlp.YoutubeDL(ytdl_options) as ytdl:
                # Search for playlist
                search_query = f"ytsearch5:{query} playlist"
                info = ytdl.extract_info(search_query, download=False)

                if 'entries' not in info or not info['entries']:
                    return None

                # Find a result that looks like a playlist or long mix, or just return top results
                urls = []
                for entry in info['entries'][:limit]:
                    if entry and entry.get('id'):
                        urls.append(f"https://www.youtube.com/watch?v={entry['id']}")

                return urls if urls else None
        except Exception as e:
            print(f"Error searching YouTube playlist: {e}")
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
