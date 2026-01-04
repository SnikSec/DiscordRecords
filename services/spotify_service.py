"""
Spotify Service
Handles integration with Spotify API for track search and playlist retrieval
"""
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import Optional, List, Dict


class SpotifyService:
    """Service for interacting with Spotify API"""
    
    def __init__(self):
        """Initialize Spotify client with credentials"""
        try:
            client_id = os.getenv('SPOTIFY_CLIENT_ID')
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
            
            if client_id and client_secret:
                auth_manager = SpotifyClientCredentials(
                    client_id=client_id,
                    client_secret=client_secret
                )
                self.spotify = spotipy.Spotify(auth_manager=auth_manager)
                self.enabled = True
                print("✅ Spotify integration enabled")
            else:
                self.spotify = None
                self.enabled = False
                print("⚠️ Spotify credentials not found - Spotify features disabled")
        except Exception as e:
            self.spotify = None
            self.enabled = False
            print(f"⚠️ Failed to initialize Spotify: {e}")
    
    async def search_track(self, query: str) -> Optional[Dict]:
        """
        Search for a track on Spotify
        
        Args:
            query: Search query (song name, artist, etc.)
            
        Returns:
            Dictionary with track information or None if not found
        """
        if not self.enabled:
            return None
        
        try:
            results = self.spotify.search(q=query, type='track', limit=1)
            
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                return {
                    'name': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'duration': track['duration_ms'] // 1000,
                    'url': track['external_urls']['spotify'],
                    'thumbnail': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'uri': track['uri']
                }
            return None
        except Exception as e:
            print(f"Error searching Spotify track: {e}")
            return None
    
    async def get_playlist_tracks(self, playlist_url_or_id: str) -> List[Dict]:
        """
        Get tracks from a Spotify playlist
        
        Args:
            playlist_url_or_id: Spotify playlist URL or ID
            
        Returns:
            List of track dictionaries
        """
        if not self.enabled:
            return []
        
        try:
            # Extract playlist ID from URL if needed
            if 'spotify.com' in playlist_url_or_id:
                playlist_id = playlist_url_or_id.split('playlist/')[-1].split('?')[0]
            else:
                playlist_id = playlist_url_or_id
            
            # Get playlist tracks
            results = self.spotify.playlist_tracks(playlist_id)
            tracks = []
            
            for item in results['items']:
                if item['track']:
                    track = item['track']
                    tracks.append({
                        'name': track['name'],
                        'artist': ', '.join([artist['name'] for artist in track['artists']]),
                        'album': track['album']['name'],
                        'duration': track['duration_ms'] // 1000,
                        'url': track['external_urls']['spotify'],
                        'uri': track['uri']
                    })
            
            return tracks
        except Exception as e:
            print(f"Error getting Spotify playlist: {e}")
            return []
    
    async def search_playlist(self, query: str) -> Optional[Dict]:
        """
        Search for a playlist on Spotify
        
        Args:
            query: Search query for playlist
            
        Returns:
            Dictionary with playlist information or None if not found
        """
        if not self.enabled:
            return None
        
        try:
            results = self.spotify.search(q=query, type='playlist', limit=1)
            
            if results['playlists']['items']:
                playlist = results['playlists']['items'][0]
                return {
                    'name': playlist['name'],
                    'description': playlist['description'],
                    'owner': playlist['owner']['display_name'],
                    'url': playlist['external_urls']['spotify'],
                    'id': playlist['id'],
                    'tracks_total': playlist['tracks']['total'],
                    'thumbnail': playlist['images'][0]['url'] if playlist['images'] else None
                }
            return None
        except Exception as e:
            print(f"Error searching Spotify playlist: {e}")
            return None
    
    async def get_recommendations(self, seed_tracks: List[str] = None, 
                                 seed_genres: List[str] = None,
                                 limit: int = 20) -> List[Dict]:
        """
        Get track recommendations from Spotify
        
        Args:
            seed_tracks: List of track IDs or URIs for recommendations
            seed_genres: List of genre seeds
            limit: Number of recommendations to return
            
        Returns:
            List of recommended track dictionaries
        """
        if not self.enabled:
            return []
        
        try:
            # Clean track URIs
            if seed_tracks:
                seed_tracks = [t.split(':')[-1] if ':' in t else t for t in seed_tracks]
            
            results = self.spotify.recommendations(
                seed_tracks=seed_tracks,
                seed_genres=seed_genres,
                limit=limit
            )
            
            tracks = []
            for track in results['tracks']:
                tracks.append({
                    'name': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'duration': track['duration_ms'] // 1000,
                    'url': track['external_urls']['spotify'],
                    'uri': track['uri']
                })
            
            return tracks
        except Exception as e:
            print(f"Error getting Spotify recommendations: {e}")
            return []
    
    async def get_available_genres(self) -> List[str]:
        """
        Get list of available genre seeds for recommendations
        
        Returns:
            List of genre strings
        """
        if not self.enabled:
            return []
        
        try:
            return self.spotify.recommendation_genre_seeds()['genres']
        except Exception as e:
            print(f"Error getting genre seeds: {e}")
            return []
