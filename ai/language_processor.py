"""
Language Processor
Uses AI to interpret natural language music requests
Supports both OpenAI and Anthropic as providers.
"""
import os
import re
from typing import Dict

try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None


class LanguageProcessor:
    """Process natural language queries for music requests"""
    
    def __init__(self):
        """Initialize the language processor with available AI provider"""
        self.provider = None
        self.client = None
        self.enabled = False

        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')

        # Prefer OpenAI if available, fall back to Anthropic
        if openai_key and openai:
            self.client = openai.OpenAI(api_key=openai_key)
            self.provider = 'openai'
            self.enabled = True
            print("✅ AI language processing enabled (OpenAI)")
        elif anthropic_key and anthropic:
            self.client = anthropic.Anthropic(api_key=anthropic_key)
            self.provider = 'anthropic'
            self.enabled = True
            print("✅ AI language processing enabled (Anthropic)")
        else:
            print("⚠️ No AI API key found - Using basic keyword matching")
        
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
        """Use AI to interpret the query (supports OpenAI and Anthropic)"""
        
        prompt = f"""Music query interpreter. Parse this request into structured format.
Request: "{query}"

Reply EXACTLY as:
TYPE: search|playlist|genre|background
QUERY: <search terms>
SOURCE: spotify|youtube
DURATION: <minutes if mentioned, else 0>

Rules: spotify for named songs/artists/playlists. youtube for mixes/ambient/vibes/background.
Use TYPE background when user wants extended/continuous play (mentions time, hours, "for a while", "background music").

Examples:
"DnD tavern music" → TYPE: genre QUERY: dungeons and dragons tavern music SOURCE: youtube DURATION: 0
"Shape of You" → TYPE: search QUERY: Shape of You Ed Sheeran SOURCE: spotify DURATION: 0
"rock workout playlist" → TYPE: playlist QUERY: rock workout SOURCE: spotify DURATION: 0
"tavern music for 4 hours" → TYPE: background QUERY: tavern music SOURCE: youtube DURATION: 240
"play chill vibes for a while" → TYPE: background QUERY: chill vibes SOURCE: youtube DURATION: 120"""

        if self.provider == 'openai':
            response_text = await self._call_openai(prompt)
        else:
            response_text = await self._call_anthropic(prompt)
        
        # Parse the response
        type_match = re.search(r'TYPE:\s*(\w+)', response_text, re.IGNORECASE)
        query_match = re.search(r'QUERY:\s*(.+?)(?:\n|$)', response_text, re.IGNORECASE)
        source_match = re.search(r'SOURCE:\s*(\w+)', response_text, re.IGNORECASE)
        duration_match = re.search(r'DURATION:\s*(\d+)', response_text, re.IGNORECASE)
        
        return {
            'type': type_match.group(1).lower() if type_match else 'search',
            'search_query': query_match.group(1).strip() if query_match else query,
            'description': query,
            'preferred_source': source_match.group(1).lower() if source_match else 'youtube',
            'duration_minutes': int(duration_match.group(1)) if duration_match else 0
        }

    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        import asyncio
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
        )
        return response.choices[0].message.content

    async def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API"""
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def _interpret_with_keywords(self, query: str) -> Dict:
        """Fallback interpretation using keyword matching"""
        query_lower = query.lower()
        
        # Check for duration/background requests
        duration_minutes = 0
        duration_match = re.search(r'(\d+)\s*hours?', query_lower)
        if duration_match:
            duration_minutes = int(duration_match.group(1)) * 60
        else:
            duration_match = re.search(r'(\d+)\s*min', query_lower)
            if duration_match:
                duration_minutes = int(duration_match.group(1))
        
        is_background = duration_minutes > 0 or any(w in query_lower for w in ['for a while', 'background', 'all night', 'all day'])
        
        if is_background:
            # Strip duration text from search query
            clean_query = re.sub(r'for\s+(\d+\s*hours?|\d+\s*min\w*|a while|all night|all day)', '', query_lower).strip()
            return {
                'type': 'background',
                'search_query': clean_query or query,
                'description': query,
                'preferred_source': 'youtube',
                'duration_minutes': duration_minutes or 120
            }
        
        # Check for activity-based requests (like "DnD tavern music")
        for activity in self.activity_keywords:
            if activity in query_lower:
                return {
                    'type': 'genre',
                    'search_query': f"{query} music",
                    'description': f"{query.title()} music",
                    'preferred_source': 'youtube',
                    'duration_minutes': 0
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
