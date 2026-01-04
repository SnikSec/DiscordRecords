"""
Music Player Module
Handles music playback, queue management, and audio streaming
"""
import asyncio
import discord
from discord.ext import commands
from typing import Optional, Dict, List
from services.spotify_service import SpotifyService
from services.youtube_service import YouTubeService
import yt_dlp


class Song:
    """Represents a song in the queue"""
    
    def __init__(self, title: str, url: str, duration: int, thumbnail: str, 
                 requester: discord.Member, source: str = "youtube"):
        self.title = title
        self.url = url
        self.duration = duration
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
        self.queues: Dict[int, List[Song]] = {}
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
        }
        
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
    
    def get_queue(self, guild_id: int) -> List[Song]:
        """Get the queue for a guild"""
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        return self.queues[guild_id]
    
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
                    await ctx.author.voice.channel.connect()
                else:
                    await ctx.send("❌ You need to be in a voice channel!")
                    return
            
            # Determine source preference
            source = interpreted_query.get('preferred_source', 'youtube')
            query_type = interpreted_query.get('type', 'search')
            search_query = interpreted_query.get('search_query', '')
            
            songs_to_add = []
            
            # Handle different query types
            if source == 'spotify' and query_type == 'playlist':
                # Get Spotify playlist
                await ctx.send(f"🔍 Fetching Spotify playlist...")
                tracks = await self.spotify.get_playlist_tracks(search_query)
                
                for track in tracks[:20]:  # Limit to 20 songs
                    # Search YouTube for each Spotify track
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
                    await ctx.send(embed=songs_to_add[0].create_embed())
            else:
                await ctx.send(f"✅ Added **{len(songs_to_add)}** songs to the queue!")
            
            # Start playing if not already playing
            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)
        
        except Exception as e:
            await ctx.send(f"❌ Error playing music: {str(e)}")
            print(f"Error in play: {e}")
    
    async def get_song_info(self, url: str) -> Optional[Dict]:
        """Extract song information from a URL"""
        try:
            with yt_dlp.YoutubeDL(self.ytdl_options) as ytdl:
                info = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: ytdl.extract_info(url, download=False)
                )
                
                # Check if it's a playlist
                if 'entries' in info:
                    return {
                        'entries': [
                            {
                                'title': entry.get('title', 'Unknown'),
                                'url': entry.get('url', entry.get('webpage_url', '')),
                                'duration': entry.get('duration', 0),
                                'thumbnail': entry.get('thumbnail', '')
                            }
                            for entry in info['entries'] if entry
                        ]
                    }
                else:
                    return {
                        'title': info.get('title', 'Unknown'),
                        'url': info.get('url', ''),
                        'duration': info.get('duration', 0),
                        'thumbnail': info.get('thumbnail', '')
                    }
        except Exception as e:
            print(f"Error extracting song info: {e}")
            return None
    
    async def play_next(self, ctx: commands.Context):
        """Play the next song in the queue"""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        if not queue:
            self.current_song[guild_id] = None
            return
        
        song = queue.pop(0)
        self.current_song[guild_id] = song
        
        try:
            # Create audio source
            audio_source = discord.FFmpegPCMAudio(song.url, **self.ffmpeg_options)
            audio_source = discord.PCMVolumeTransformer(audio_source, volume=self.get_volume(guild_id))
            
            # Play the song
            ctx.voice_client.play(
                audio_source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(ctx), self.bot.loop
                )
            )
        except Exception as e:
            print(f"Error playing song: {e}")
            await ctx.send(f"❌ Error playing: {song.title}")
            await self.play_next(ctx)
    
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
        """Stop playback and clear the queue"""
        guild_id = ctx.guild.id
        
        if guild_id in self.queues:
            self.queues[guild_id].clear()
        
        self.current_song[guild_id] = None
        
        if ctx.voice_client:
            ctx.voice_client.stop()
        
        await ctx.send("⏹️ Stopped playback and cleared the queue")
    
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
