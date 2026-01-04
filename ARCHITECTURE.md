# DiscordRecords Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       Discord User                          │
│                  (Voice Channel + Text)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Natural Language Request
                     │ "Play DnD tavern music"
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      bot.py (Main)                          │
│                  Discord Bot Interface                      │
│              Command Handlers & Events                      │
└─────┬──────────────────────────────┬────────────────────────┘
      │                              │
      │ Interpret Query              │ Playback Control
      ▼                              ▼
┌──────────────────────┐   ┌─────────────────────────────────┐
│  language_processor  │   │      music/player.py            │
│  (AI Integration)    │   │   Music Player & Queue          │
│  - Claude API        │   │   - FFmpeg Audio                │
│  - Keyword Matching  │   │   - Voice Client                │
└──────┬───────────────┘   └────┬──────────┬─────────────────┘
       │                        │          │
       │ Interpreted Query      │          │
       └────────────────────────┘          │
                                            │
                    ┌───────────────────────┴─────────────┐
                    │                                     │
                    ▼                                     ▼
        ┌──────────────────────┐           ┌──────────────────────┐
        │ spotify_service.py   │           │ youtube_service.py   │
        │  Spotify API         │           │  YouTube Search      │
        │  - Search Tracks     │           │  - yt-dlp            │
        │  - Get Playlists     │           │  - Video Info        │
        │  - Recommendations   │           │  - Audio Stream      │
        └──────────────────────┘           └──────────────────────┘
                    │                                     │
                    │ Track Info                          │ Stream URL
                    └─────────────────┬───────────────────┘
                                      ▼
                            ┌─────────────────────┐
                            │   Discord Voice     │
                            │   (Audio Output)    │
                            └─────────────────────┘
```

## Component Breakdown

### 1. bot.py (Main Entry Point)
**Responsibilities:**
- Initialize Discord bot with proper intents
- Register command handlers
- Manage bot lifecycle and events
- Route commands to appropriate modules

**Key Commands:**
- `!play <query>` → MusicPlayer.play()
- `!pause` / `!resume` → MusicPlayer.pause/resume()
- `!skip` → MusicPlayer.skip()
- `!queue` → MusicPlayer.show_queue()

### 2. ai/language_processor.py
**Responsibilities:**
- Interpret natural language music requests
- Use Claude AI for advanced understanding
- Fall back to keyword matching if AI unavailable
- Determine query type and preferred source

**Input:** "Play some DnD tavern music"
**Output:**
```python
{
    'type': 'genre',
    'search_query': 'dungeons and dragons tavern medieval fantasy music',
    'description': 'Fantasy tavern background music',
    'preferred_source': 'youtube'
}
```

### 3. music/player.py
**Responsibilities:**
- Manage music queue per guild
- Handle voice client connections
- Control playback (play, pause, skip, stop)
- Stream audio using FFmpeg
- Display now playing information

**Key Features:**
- Guild-specific queues
- Automatic song progression
- Volume control
- Rich Discord embeds

### 4. services/spotify_service.py
**Responsibilities:**
- Interface with Spotify API
- Search for tracks and playlists
- Get track information
- Provide recommendations

**API Operations:**
- `search_track(query)` → Track info
- `get_playlist_tracks(url)` → List of tracks
- `search_playlist(query)` → Playlist info
- `get_recommendations(seeds)` → Recommended tracks

### 5. services/youtube_service.py
**Responsibilities:**
- Search YouTube for videos
- Extract video information
- Get streamable audio URLs

**Uses:**
- yt-dlp for YouTube interaction
- Extracts best audio quality
- Handles playlists

## Data Flow Example

### User Request: "!play DnD tavern music"

1. **bot.py** receives command
   ```python
   @bot.command(name='play')
   async def play(ctx, *, query: str):
   ```

2. **language_processor** interprets request
   ```python
   interpreted = await language_processor.interpret_query(query)
   # Returns: {type: 'genre', search_query: 'dungeons dragons tavern music', ...}
   ```

3. **player.py** determines source
   ```python
   if source == 'youtube':
       url = await youtube.search(search_query)
   ```

4. **youtube_service** finds video
   ```python
   # Searches YouTube, returns video URL
   "https://youtube.com/watch?v=abc123"
   ```

5. **player.py** extracts audio stream
   ```python
   song_info = await get_song_info(url)
   # Uses yt-dlp to get streamable URL
   ```

6. **player.py** plays audio
   ```python
   audio_source = discord.FFmpegPCMAudio(song.url)
   ctx.voice_client.play(audio_source)
   ```

## Module Dependencies

```
bot.py
├── discord.py (Discord API)
├── music/player.py
│   ├── services/spotify_service.py
│   │   └── spotipy
│   └── services/youtube_service.py
│       └── yt-dlp
└── ai/language_processor.py
    └── anthropic (Claude API)
```

## Configuration Flow

```
Environment Variables (.env)
├── DISCORD_TOKEN → bot.py
├── SPOTIFY_CLIENT_ID → spotify_service.py
├── SPOTIFY_CLIENT_SECRET → spotify_service.py
└── ANTHROPIC_API_KEY → language_processor.py
```

## State Management

### Per-Guild State (music/player.py)
```python
self.queues: Dict[guild_id, List[Song]]
self.current_song: Dict[guild_id, Song]
self.volume: Dict[guild_id, float]
```

Each Discord server (guild) maintains its own:
- Music queue
- Currently playing song
- Volume setting
- Voice client connection

## Error Handling Strategy

1. **Graceful Degradation**
   - Missing Spotify credentials → YouTube only
   - Missing AI key → Keyword matching
   - FFmpeg not found → Clear error message

2. **User Feedback**
   - All errors shown to user in Discord
   - Detailed logs in console
   - Helpful error messages with suggestions

3. **Automatic Recovery**
   - Connection drops → Auto-reconnect
   - Song fails → Skip to next
   - API rate limits → Wait and retry

## Extension Points

### Adding a New Music Source

1. Create `services/newsource_service.py`
2. Implement search and get_info methods
3. Update `player.py` to check new source
4. Add to `language_processor.py` source detection

### Adding New AI Providers

1. Update `ai/language_processor.py`
2. Add new API client initialization
3. Implement interpretation method
4. Add fallback logic

### Adding New Commands

1. Add command handler in `bot.py`
2. Implement logic in `player.py` or new module
3. Update help command
4. Document in README.md
