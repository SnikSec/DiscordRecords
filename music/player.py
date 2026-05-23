"""
Music Player Module
Handles music playback, queue management, and audio streaming
"""
import asyncio
import os
import discord
from discord.ext import commands
from typing import Optional, Dict, List
from services.spotify_service import SpotifyService
from services.youtube_service import YouTubeService
import yt_dlp

# Use local ffmpeg bundled with the repo
FFMPEG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ffmpeg.exe')


class Song:
    """Represents a song in the queue"""
    
    def __init__(self, title: str, url: str, duration: int, thumbnail: str, 
                 requester: discord.Member, source: str = "youtube"):
        self.title = title
        self.url = url
        self.duration = int(duration or 0)
        self.thumbnail = thumbnail
        self.requester = requester
        self.source = source
    
    def format_duration(self) -> str:
        """Format duration in minutes:seconds"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"
    
    def create_embed(self) -> discord.Embed:
        """Create a Discord embed for this song"""
        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{self.title}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Duration", value=self.format_duration(), inline=True)
        embed.add_field(name="Source", value=self.source.title(), inline=True)
        embed.add_field(name="Requested by", value=self.requester.mention, inline=True)
        
        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)
        
        return embed


class MusicPlayer:
    """Main music player class"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.spotify = SpotifyService()
        self.youtube = YouTubeService()
        
        # Guild-specific queues and state
        self.queues: Dict[int, List[Song]] = {}  # User queue (priority)
        self.background_queues: Dict[int, List[Song]] = {}  # Background queue (auto-filled)
        self.background_theme: Dict[int, str] = {}  # Current background search theme
        self.current_song: Dict[int, Optional[Song]] = {}
        self.volume: Dict[int, float] = {}
        
        # yt-dlp options for downloading/streaming
        self.ytdl_options = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': False,  # Allow playlists
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'age_limit': 99,
            'geo_bypass': True,
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            'remote_components': 'ejs:github',
        }
        
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
    
    def get_queue(self, guild_id: int) -> List[Song]:
        """Get the user queue for a guild (priority)"""
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        return self.queues[guild_id]
    
    def get_background_queue(self, guild_id: int) -> List[Song]:
        """Get the background queue for a guild"""
        if guild_id not in self.background_queues:
            self.background_queues[guild_id] = []
        return self.background_queues[guild_id]
    
    def get_volume(self, guild_id: int) -> float:
        """Get the volume for a guild"""
        return self.volume.get(guild_id, 0.5)
    
    async def play(self, ctx: commands.Context, interpreted_query: Dict):
        """Play music based on an interpreted query"""
        guild_id = ctx.guild.id
        
        try:
            # Check if we need to join the voice channel
            if not ctx.voice_client:
                if ctx.author.voice:
                    try:
                        await ctx.author.voice.channel.connect(self_deaf=True, timeout=15.0)
                    except Exception as e:
                        await ctx.send(f"❌ Failed to connect to voice channel: {e}")
                        return
                else:
                    await ctx.send("❌ You need to be in a voice channel!")
                    return
            elif not ctx.voice_client.is_connected():
                await ctx.voice_client.disconnect(force=True)
                try:
                    await ctx.author.voice.channel.connect(self_deaf=True, timeout=15.0)
                except Exception as e:
                    await ctx.send(f"❌ Failed to reconnect to voice channel: {e}")
                    return
            
            # Determine source preference
            source = interpreted_query.get('preferred_source', 'youtube')
            query_type = interpreted_query.get('type', 'search')
            search_query = interpreted_query.get('search_query', '')
            
            # Treat background as genre for !play (background only via !background command)
            if query_type == 'background':
                query_type = 'genre'
            
            songs_to_add = []
            
            # Handle different query types
            if source == 'spotify' and query_type == 'playlist':
                # Search Spotify for playlist by name, then resolve tracks via YouTube
                if self.spotify.enabled:
                    await ctx.send(f"🔍 Searching Spotify playlists for: {search_query}")
                    playlist_info = await self.spotify.search_playlist(search_query)
                    
                    if playlist_info:
                        await ctx.send(f"📋 Found playlist: **{playlist_info['name']}** ({playlist_info['tracks_total']} tracks)")
                        tracks = await self.spotify.get_playlist_tracks(playlist_info['id'])
                        
                        for track in tracks[:20]:  # Limit to 20 songs
                            yt_url = await self.youtube.search(f"{track['name']} {track['artist']}")
                            if yt_url:
                                song_info = await self.get_song_info(yt_url)
                                if song_info:
                                    song = Song(
                                        title=f"{track['name']} - {track['artist']}",
                                        url=song_info['url'],
                                        duration=song_info['duration'],
                                        thumbnail=song_info['thumbnail'],
                                        requester=ctx.author,
                                        source='spotify'
                                    )
                                    songs_to_add.append(song)
                    else:
                        await ctx.send("⚠️ No Spotify playlist found, trying YouTube...")
                        # Fall through to YouTube playlist search below
                
                # If Spotify disabled or no results, try YouTube playlist search
                if not songs_to_add:
                    urls = await self.youtube.search_playlist(search_query)
                    if urls:
                        await ctx.send(f"🔍 Queuing {len(urls)} songs from YouTube...")
                        for url in urls:
                            song_info = await self.get_song_info(url)
                            if song_info and 'entries' not in song_info:
                                song = Song(
                                    title=song_info['title'],
                                    url=song_info['url'],
                                    duration=song_info['duration'],
                                    thumbnail=song_info['thumbnail'],
                                    requester=ctx.author,
                                    source='youtube'
                                )
                                songs_to_add.append(song)
            
            elif source == 'spotify' and query_type == 'search':
                # Search Spotify and play on YouTube
                await ctx.send(f"🔍 Searching Spotify for: {search_query}")
                track = await self.spotify.search_track(search_query)
                
                if track:
                    # Find on YouTube
                    yt_url = await self.youtube.search(f"{track['name']} {track['artist']}")
                    if yt_url:
                        song_info = await self.get_song_info(yt_url)
                        if song_info:
                            song = Song(
                                title=song_info['title'],
                                url=song_info['url'],
                                duration=song_info['duration'],
                                thumbnail=song_info['thumbnail'],
                                requester=ctx.author,
                                source='spotify'
                            )
                            songs_to_add.append(song)
                
                # Fallback to YouTube if Spotify didn't find anything
                if not songs_to_add:
                    await ctx.send("⚠️ Not found on Spotify, searching YouTube...")
                    url = await self.youtube.search(search_query)
                    if url:
                        song_info = await self.get_song_info(url)
                        if song_info:
                            song = Song(
                                title=song_info['title'],
                                url=song_info['url'],
                                duration=song_info['duration'],
                                thumbnail=song_info['thumbnail'],
                                requester=ctx.author,
                                source='youtube'
                            )
                            songs_to_add.append(song)

            elif query_type == 'playlist':
                # YouTube playlist search by name
                await ctx.send(f"🔍 Searching YouTube playlists for: {search_query}")
                urls = await self.youtube.search_playlist(search_query)
                if urls:
                    await ctx.send(f"📋 Queuing {len(urls)} songs...")
                    for url in urls:
                        song_info = await self.get_song_info(url)
                        if song_info and 'entries' not in song_info:
                            song = Song(
                                title=song_info['title'],
                                url=song_info['url'],
                                duration=song_info['duration'],
                                thumbnail=song_info['thumbnail'],
                                requester=ctx.author,
                                source='youtube'
                            )
                            songs_to_add.append(song)
            
            else:  # YouTube search or URL
                await ctx.send(f"🔍 Searching YouTube...")
                
                if query_type == 'url':
                    url = search_query
                else:
                    url = await self.youtube.search(search_query)
                
                if url:
                    song_info = await self.get_song_info(url)
                    if song_info:
                        # Check if it's a playlist
                        if 'entries' in song_info:
                            for entry in song_info['entries'][:20]:
                                song = Song(
                                    title=entry['title'],
                                    url=entry['url'],
                                    duration=entry.get('duration', 0),
                                    thumbnail=entry.get('thumbnail', ''),
                                    requester=ctx.author,
                                    source='youtube'
                                )
                                songs_to_add.append(song)
                        else:
                            song = Song(
                                title=song_info['title'],
                                url=song_info['url'],
                                duration=song_info['duration'],
                                thumbnail=song_info['thumbnail'],
                                requester=ctx.author,
                                source='youtube'
                            )
                            songs_to_add.append(song)
            
            if not songs_to_add:
                await ctx.send("❌ Could not find any songs matching your request!")
                return
            
            # Add songs to queue
            queue = self.get_queue(guild_id)
            queue.extend(songs_to_add)
            
            # Send confirmation
            if len(songs_to_add) == 1:
                if ctx.voice_client.is_playing():
                    await ctx.send(f"✅ Added to queue: **{songs_to_add[0].title}**")
            else:
                await ctx.send(f"✅ Added **{len(songs_to_add)}** songs to the queue!")
            
            # If background music is playing, interrupt it to play user's request
            current = self.current_song.get(guild_id)
            is_background_playing = (
                ctx.voice_client.is_playing() and
                current and current.source == 'background'
            )
            
            if is_background_playing:
                # Put current background song back in background queue
                bg_queue = self.get_background_queue(guild_id)
                bg_queue.insert(0, current)
                ctx.voice_client.stop()  # This triggers after callback → play_next → picks user queue
            elif not ctx.voice_client.is_playing():
                await self.play_next(ctx)
        
        except Exception as e:
            await ctx.send(f"❌ Error playing music: {str(e)}")
            print(f"Error in play: {e}")
    
    async def get_song_info(self, url: str) -> Optional[Dict]:
        """Extract song information from a URL"""
        try:
            # For playlists/mixes, use flat extraction to get entries quickly
            is_playlist = 'list=' in url
            opts = dict(self.ytdl_options)
            if is_playlist:
                opts['extract_flat'] = True
                opts['playlistend'] = 25  # Cap at 25 songs for radio/mixes

            with yt_dlp.YoutubeDL(opts) as ytdl:
                info = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: ytdl.extract_info(url, download=False)
                )
                
                # Check if it's a playlist
                if 'entries' in info:
                    entries = []
                    for entry in info['entries']:
                        if not entry:
                            continue
                        video_url = entry.get('url') or entry.get('webpage_url') or ''
                        # For flat extraction, build URL from ID
                        if not video_url and entry.get('id'):
                            video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                        entries.append({
                            'title': entry.get('title', 'Unknown'),
                            'url': video_url,
                            'duration': entry.get('duration', 0),
                            'thumbnail': entry.get('thumbnail', '')
                        })
                    return {'entries': entries}
                else:
                    return {
                        'title': info.get('title', 'Unknown'),
                        'url': info.get('url', '') or url,  # Fall back to page URL
                        'duration': info.get('duration', 0),
                        'thumbnail': info.get('thumbnail', '')
                    }
        except Exception as e:
            print(f"Error extracting song info: {e}")
            # For direct URLs, return basic info so play_next can try to extract the stream
            if 'youtube.com/watch' in url or 'youtu.be/' in url:
                return {
                    'title': 'YouTube Video',
                    'url': url,
                    'duration': 0,
                    'thumbnail': ''
                }
            return None
    
    async def play_next(self, ctx: commands.Context):
        """Play the next song in the queue. User queue takes priority over background."""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        bg_queue = self.get_background_queue(guild_id)
        
        # Priority: user queue first, then background queue
        if queue:
            song = queue.pop(0)
        elif bg_queue:
            song = bg_queue.pop(0)
            # Refill background queue if running low
            if len(bg_queue) < 3 and self.background_theme.get(guild_id):
                asyncio.create_task(self._refill_background_queue(ctx))
        else:
            self.current_song[guild_id] = None
            return
        
        self.current_song[guild_id] = song
        
        try:
            # If the URL is a YouTube page URL (not a direct stream), extract the stream URL
            stream_url = song.url
            if 'youtube.com/watch' in stream_url or 'youtu.be/' in stream_url or not stream_url:
                opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                }
                with yt_dlp.YoutubeDL(opts) as ytdl:
                    info = await asyncio.get_event_loop().run_in_executor(
                        None, lambda: ytdl.extract_info(stream_url, download=False)
                    )
                    stream_url = info.get('url', '')
                    if not song.duration and info.get('duration'):
                        song.duration = info['duration']
                    if not song.thumbnail and info.get('thumbnail'):
                        song.thumbnail = info['thumbnail']
            
            if not stream_url:
                print(f"Could not get stream URL for: {song.title}")
                await ctx.send(f"⚠️ Skipping (no stream): {song.title}")
                await self.play_next(ctx)
                return

            # Don't try to play if already playing
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                # Put song back at front of queue
                queue.insert(0, song)
                return

            # Create audio source
            audio_source = discord.FFmpegPCMAudio(stream_url, executable=FFMPEG_PATH, **self.ffmpeg_options)
            audio_source = discord.PCMVolumeTransformer(audio_source, volume=self.get_volume(guild_id))
            
            # Play the song
            ctx.voice_client.play(
                audio_source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(ctx), self.bot.loop
                )
            )
            
            await ctx.send(embed=song.create_embed())
        except Exception as e:
            print(f"Error playing song: {e}")
            await ctx.send(f"❌ Error playing: {song.title}")
            # Only advance if not already playing something
            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)
    
    async def _start_background_play(self, ctx: commands.Context, theme: str, duration_minutes: int):
        """Start background/continuous music playback"""
        guild_id = ctx.guild.id
        duration_minutes = duration_minutes or 120  # Default 2 hours
        
        # First, try to find a long mix video matching the duration
        long_query = f"{theme} {duration_minutes // 60} hour mix"
        await ctx.send(f"🎶 Setting up background music: **{theme}** (~{duration_minutes // 60}h)")
        
        url = await self.youtube.search(long_query, music_only=False)
        if url:
            # Check if it's actually long enough
            info = await self.youtube.get_video_info(url)
            if info and info.get('duration', 0) >= duration_minutes * 30:  # At least half the requested time
                song = Song(
                    title=info['title'],
                    url=url,
                    duration=int(info.get('duration', 0)),
                    thumbnail=info.get('thumbnail', ''),
                    requester=ctx.author,
                    source='background'
                )
                bg_queue = self.get_background_queue(guild_id)
                bg_queue.append(song)
                self.background_theme[guild_id] = theme
                
                if not ctx.voice_client.is_playing():
                    await self.play_next(ctx)
                else:
                    await ctx.send(f"✅ Background music queued: **{info['title']}**")
                return
        
        # Fallback: fill background queue with multiple similar songs
        self.background_theme[guild_id] = theme
        await self._refill_background_queue(ctx, initial=True)
        
        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)
    
    async def _refill_background_queue(self, ctx, initial: bool = False):
        """Refill the background queue with songs matching the theme"""
        guild_id = ctx.guild.id
        theme = self.background_theme.get(guild_id, '')
        if not theme:
            return
        
        bg_queue = self.get_background_queue(guild_id)
        
        # Search for several variations
        search_terms = [
            f"{theme} mix",
            f"{theme} playlist",
            f"{theme} compilation",
            f"best {theme}",
            f"{theme} music",
        ]
        
        count = 0
        target = 10 if initial else 5
        for term in search_terms:
            if count >= target:
                break
            url = await self.youtube.search(term, limit=5, music_only=False)
            if url:
                # Make sure we don't add duplicates
                existing_urls = [s.url for s in bg_queue]
                if url not in existing_urls:
                    song = Song(
                        title=f"[BG] {term}",
                        url=url,
                        duration=0,
                        thumbnail='',
                        requester=ctx.author,
                        source='background'
                    )
                    bg_queue.append(song)
                    count += 1
        
        if initial and count > 0:
            await ctx.send(f"✅ Queued **{count}** background tracks for: **{theme}**\n💡 Your `!play` requests will always take priority!")

    async def pause(self, ctx: commands.Context):
        """Pause the current playback"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Paused playback")
        else:
            await ctx.send("❌ Nothing is playing!")
    
    async def resume(self, ctx: commands.Context):
        """Resume paused playback"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Resumed playback")
        else:
            await ctx.send("❌ Playback is not paused!")
    
    async def skip(self, ctx: commands.Context):
        """Skip the current song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ Skipped!")
        else:
            await ctx.send("❌ Nothing is playing!")
    
    async def stop(self, ctx: commands.Context):
        """Stop playback and clear all queues"""
        guild_id = ctx.guild.id
        
        if guild_id in self.queues:
            self.queues[guild_id].clear()
        if guild_id in self.background_queues:
            self.background_queues[guild_id].clear()
        self.background_theme.pop(guild_id, None)
        
        self.current_song[guild_id] = None
        
        if ctx.voice_client:
            ctx.voice_client.stop()
        
        await ctx.send("⏹️ Stopped playback and cleared all queues")
    
    async def show_queue(self, ctx: commands.Context):
        """Display the current queue"""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        current = self.current_song.get(guild_id)
        
        if not current and not queue:
            await ctx.send("📋 Queue is empty!")
            return
        
        embed = discord.Embed(
            title="📋 Music Queue",
            color=discord.Color.blue()
        )
        
        if current:
            embed.add_field(
                name="🎵 Now Playing",
                value=f"**{current.title}** ({current.format_duration()})\nRequested by {current.requester.mention}",
                inline=False
            )
        
        if queue:
            queue_text = "\n".join([
                f"`{i+1}.` **{song.title}** ({song.format_duration()})"
                for i, song in enumerate(queue[:10])
            ])
            
            if len(queue) > 10:
                queue_text += f"\n\n*...and {len(queue) - 10} more songs*"
            
            embed.add_field(
                name="⏭️ Up Next",
                value=queue_text,
                inline=False
            )
            embed.set_footer(text=f"Total songs in queue: {len(queue)}")
        
        await ctx.send(embed=embed)
    
    async def now_playing(self, ctx: commands.Context):
        """Display the currently playing song"""
        guild_id = ctx.guild.id
        current = self.current_song.get(guild_id)
        
        if current:
            await ctx.send(embed=current.create_embed())
        else:
            await ctx.send("❌ Nothing is currently playing!")
    
    async def set_volume(self, ctx: commands.Context, volume: int):
        """Set the playback volume"""
        guild_id = ctx.guild.id
        volume_float = volume / 100
        
        self.volume[guild_id] = volume_float
        
        if ctx.voice_client and ctx.voice_client.source:
            ctx.voice_client.source.volume = volume_float
        
        await ctx.send(f"🔊 Volume set to {volume}%")
    
    async def leave(self, ctx: commands.Context):
        """Disconnect from the voice channel"""
        guild_id = ctx.guild.id
        
        # Clear queue and current song
        if guild_id in self.queues:
            self.queues[guild_id].clear()
        self.current_song[guild_id] = None
        
        # Disconnect
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Disconnected from voice channel")
        else:
            await ctx.send("❌ Not connected to a voice channel!")
