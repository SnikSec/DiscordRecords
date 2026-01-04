"""
Language Processor
Uses AI to interpret natural language music requests
"""
import os
import re
from typing import Dict
import anthropic


class LanguageProcessor:
    """Process natural language queries for music requests"""
    
    def __init__(self):
        """Initialize the language processor"""
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.enabled = True
            print("✅ AI language processing enabled")
        else:
            self.client = None
            self.enabled = False
            print("⚠️ ANTHROPIC_API_KEY not found - Using basic keyword matching")
        
        # Keyword patterns for fallback
        self.genre_keywords = {
            'dnb', 'drum and bass', 'jazz', 'rock', 'pop', 'classical', 'electronic',
            'hip hop', 'rap', 'country', 'folk', 'blues', 'metal', 'indie', 'r&b',
            'soul', 'funk', 'disco', 'house', 'techno', 'trance', 'dubstep', 'lofi',
            'lo-fi', 'ambient', 'chill', 'relaxing', 'edm', 'punk', 'reggae', 'ska'
        }
        
        self.mood_keywords = {
            'sad', 'happy', 'energetic', 'calm', 'angry', 'romantic', 'party',
            'workout', 'study', 'sleep', 'focus', 'upbeat', 'mellow', 'intense',
            'peaceful', 'dark', 'bright', 'chill', 'hype'
        }
        
        self.activity_keywords = {
            'tavern', 'dnd', 'd&d', 'dungeons and dragons', 'fantasy', 'medieval',
            'gaming', 'cooking', 'driving', 'running', 'yoga', 'meditation',
            'reading', 'working', 'studying', 'cleaning', 'party'
        }
    
    async def interpret_query(self, query: str) -> Dict:
        """
        Interpret a natural language music request
        
        Args:
            query: The user's natural language request
            
        Returns:
            Dictionary containing:
                - type: 'search', 'playlist', 'genre', 'mood', 'url'
                - search_query: The interpreted search query
                - description: Human-readable description
                - preferred_source: 'spotify' or 'youtube'
        """
        # Check if it's a URL
        if self._is_url(query):
            return {
                'type': 'url',
                'search_query': query,
                'description': 'Direct URL',
                'preferred_source': 'spotify' if 'spotify.com' in query else 'youtube'
            }
        
        # Use AI if enabled
        if self.enabled:
            try:
                return await self._interpret_with_ai(query)
            except Exception as e:
                print(f"Error using AI interpretation, falling back to keywords: {e}")
        
        # Fallback to keyword matching
        return self._interpret_with_keywords(query)
    
    async def _interpret_with_ai(self, query: str) -> Dict:
        """Use Claude to interpret the query"""
        
        prompt = f"""You are a music query interpreter for a Discord bot that plays music from Spotify and YouTube.

Analyze this user request and provide a structured interpretation:
"{query}"

Your response should help the bot understand:
1. What type of request this is (specific song, playlist, genre/mood, artist)
2. What to search for
3. Whether Spotify or YouTube would be better

Respond in this exact format:
TYPE: [search/playlist/genre/mood]
QUERY: [the exact search query to use]
DESCRIPTION: [brief description of what the user wants]
SOURCE: [spotify/youtube]

Examples:
- "play some DnD tavern music" → TYPE: genre, QUERY: dungeons and dragons tavern medieval fantasy music, DESCRIPTION: Fantasy tavern background music, SOURCE: youtube
- "play Shape of You" → TYPE: search, QUERY: Shape of You Ed Sheeran, DESCRIPTION: Shape of You by Ed Sheeran, SOURCE: spotify
- "chill lofi beats" → TYPE: genre, QUERY: lofi hip hop chill beats, DESCRIPTION: Relaxing lo-fi hip hop, SOURCE: youtube
- "play my Discover Weekly" → TYPE: playlist, QUERY: Discover Weekly, DESCRIPTION: Spotify Discover Weekly playlist, SOURCE: spotify

Now analyze: "{query}" """

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response = message.content[0].text
        
        # Parse the response
        type_match = re.search(r'TYPE:\s*(\w+)', response, re.IGNORECASE)
        query_match = re.search(r'QUERY:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
        desc_match = re.search(r'DESCRIPTION:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
        source_match = re.search(r'SOURCE:\s*(\w+)', response, re.IGNORECASE)
        
        return {
            'type': type_match.group(1).lower() if type_match else 'search',
            'search_query': query_match.group(1).strip() if query_match else query,
            'description': desc_match.group(1).strip() if desc_match else query,
            'preferred_source': source_match.group(1).lower() if source_match else 'youtube'
        }
    
    def _interpret_with_keywords(self, query: str) -> Dict:
        """Fallback interpretation using keyword matching"""
        query_lower = query.lower()
        
        # Check for activity-based requests (like "DnD tavern music")
        for activity in self.activity_keywords:
            if activity in query_lower:
                return {
                    'type': 'genre',
                    'search_query': f"{query} music",
                    'description': f"{query.title()} music",
                    'preferred_source': 'youtube'
                }
        
        # Check for genre keywords
        for genre in self.genre_keywords:
            if genre in query_lower:
                return {
                    'type': 'genre',
                    'search_query': f"{query} music",
                    'description': f"{genre.title()} music",
                    'preferred_source': 'youtube'
                }
        
        # Check for mood keywords
        for mood in self.mood_keywords:
            if mood in query_lower:
                return {
                    'type': 'mood',
                    'search_query': f"{query} music",
                    'description': f"{mood.title()} music",
                    'preferred_source': 'youtube'
                }
        
        # Check for playlist indicators
        if any(word in query_lower for word in ['playlist', 'mix', 'compilation', 'radio']):
            return {
                'type': 'playlist',
                'search_query': query,
                'description': query,
                'preferred_source': 'youtube'
            }
        
        # Default to search
        return {
            'type': 'search',
            'search_query': query,
            'description': query,
            'preferred_source': 'youtube'
        }
    
    def _is_url(self, query: str) -> bool:
        """Check if the query is a URL"""
        url_patterns = [
            r'https?://',
            r'youtube\.com',
            r'youtu\.be',
            r'spotify\.com'
        ]
        return any(re.search(pattern, query, re.IGNORECASE) for pattern in url_patterns)
