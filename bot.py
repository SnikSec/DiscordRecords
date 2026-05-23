"""
DiscordRecords - AI-Powered Music Bot
Main bot file with Discord integration
"""
import os
import json
import certifi
import discord
from discord.ext import commands
from music.player import MusicPlayer
from ai.language_processor import LanguageProcessor

# Fix SSL certificate verification on Windows
os.environ['SSL_CERT_FILE'] = certifi.where()

# Load config.json
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
if not os.path.exists(config_path):
    print("❌ config.json not found! Run setup.py first.")
    exit(1)

with open(config_path, 'r') as f:
    config = json.load(f)

os.environ['DISCORD_TOKEN'] = config.get('discord_token', '')
os.environ['BOT_PREFIX'] = config.get('bot_prefix', '!')
spotify = config.get('spotify', {})
os.environ['SPOTIFY_CLIENT_ID'] = spotify.get('client_id', '')
os.environ['SPOTIFY_CLIENT_SECRET'] = spotify.get('client_secret', '')
openai_cfg = config.get('openai', {})
os.environ['OPENAI_API_KEY'] = openai_cfg.get('api_key', '')
anthropic_cfg = config.get('anthropic', {})
os.environ['ANTHROPIC_API_KEY'] = anthropic_cfg.get('api_key', '')

# Bot setup with proper intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(
    command_prefix=os.getenv('BOT_PREFIX', '!'),
    intents=intents,
    description='AI-Powered Music Bot for Discord with Spotify and YouTube support'
)

# Initialize components
music_player = MusicPlayer(bot)
language_processor = LanguageProcessor()


@bot.event
async def on_ready():
    """Called when the bot is ready"""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{os.getenv('BOT_PREFIX', '!')}play [song request]"
        )
    )


@bot.event
async def on_command_error(ctx, error):
    """Global error handler"""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param.name}")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"❌ An error occurred: {str(error.original)}")
    else:
        await ctx.send(f"❌ Error: {str(error)}")
        print(f"Error: {error}")


@bot.command(name='play', aliases=['p'])
async def play(ctx, *, query: str):
    """
    Play music based on a natural language query
    Examples:
        !play DnD tavern music
        !play some chill lo-fi beats
        !play Shape of You by Ed Sheeran
    """
    # Check if user is in a voice channel
    if not ctx.author.voice:
        await ctx.send("❌ You need to be in a voice channel to play music!")
        return
    
    # Send processing message
    processing_msg = await ctx.send(f"🤖 Understanding your request: '{query}'...")
    
    try:
        # Process the natural language query
        interpreted_query = await language_processor.interpret_query(query)
        
        # Update message with interpretation
        await processing_msg.edit(
            content=f"🎵 Searching for: {interpreted_query['description']}\n"
                    f"🔍 Type: {interpreted_query['type']}"
        )
        
        # Play the music
        await music_player.play(ctx, interpreted_query)
        
    except Exception as e:
        await processing_msg.edit(content=f"❌ Error processing request: {str(e)}")
        print(f"Error in play command: {e}")


@bot.command(name='pause')
async def pause(ctx):
    """Pause the current playback"""
    await music_player.pause(ctx)


@bot.command(name='background', aliases=['bg'])
async def background(ctx, *, query: str = None):
    """
    Set background music that plays when the queue is empty.
    User queue (!play) always takes priority.
    
    Examples:
        !background tavern music
        !background chill lofi
        !background stop
        !background (shows current theme)
    """
    if not ctx.author.voice:
        await ctx.send("❌ You need to be in a voice channel!")
        return
    
    guild_id = ctx.guild.id
    
    if query is None:
        # Show current background theme
        theme = music_player.background_theme.get(guild_id)
        if theme:
            await ctx.send(f"🎶 Current background theme: **{theme}**")
        else:
            await ctx.send("No background music set. Use `!background <theme>` to set one.")
        return
    
    if query.lower() == 'stop':
        music_player.background_queues.pop(guild_id, None)
        music_player.background_theme.pop(guild_id, None)
        await ctx.send("⏹️ Background music stopped.")
        return
    
    # Connect to voice if needed
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect(self_deaf=True, timeout=15.0)
    
    # Parse duration if included
    import re
    duration_minutes = 0
    duration_match = re.search(r'(\d+)\s*hours?', query.lower())
    if duration_match:
        duration_minutes = int(duration_match.group(1)) * 60
        query = re.sub(r'for\s+\d+\s*hours?', '', query).strip()
    
    await music_player._start_background_play(ctx, query, duration_minutes)


@bot.command(name='resume')
async def resume(ctx):
    """Resume paused playback"""
    await music_player.resume(ctx)


@bot.command(name='skip', aliases=['next'])
async def skip(ctx):
    """Skip to the next song in the queue"""
    await music_player.skip(ctx)


@bot.command(name='stop')
async def stop(ctx):
    """Stop playback and clear the queue"""
    await music_player.stop(ctx)


@bot.command(name='queue', aliases=['q'])
async def queue(ctx):
    """Display the current music queue"""
    await music_player.show_queue(ctx)


@bot.command(name='nowplaying', aliases=['np', 'current'])
async def nowplaying(ctx):
    """Display information about the currently playing song"""
    await music_player.now_playing(ctx)


@bot.command(name='volume', aliases=['vol'])
async def volume(ctx, volume: int):
    """
    Set the playback volume (0-100)
    Example: !volume 50
    """
    if 0 <= volume <= 100:
        await music_player.set_volume(ctx, volume)
    else:
        await ctx.send("❌ Volume must be between 0 and 100!")


@bot.command(name='leave', aliases=['disconnect', 'dc'])
async def leave(ctx):
    """Disconnect the bot from the voice channel"""
    await music_player.leave(ctx)


@bot.command(name='join')
async def join(ctx):
    """Join the voice channel you're currently in"""
    if not ctx.author.voice:
        await ctx.send("❌ You need to be in a voice channel!")
        return
    
    channel = ctx.author.voice.channel
    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    
    await ctx.send(f"✅ Joined {channel.name}")


@bot.command(name='help_music', aliases=['musichelp'])
async def help_music(ctx):
    """Display help information for music commands"""
    embed = discord.Embed(
        title="🎵 DiscordRecords - Music Bot Commands",
        description="AI-powered music bot with natural language understanding",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🎵 Play Music",
        value="**!play** or **!p** `<query>`\n"
              "Use natural language to describe what you want to hear!\n"
              "Examples:\n"
              "• `!play DnD tavern music`\n"
              "• `!play chill lo-fi beats`\n"
              "• `!play Bohemian Rhapsody`",
        inline=False
    )
    
    embed.add_field(
        name="⏯️ Playback Controls",
        value="**!pause** - Pause playback\n"
              "**!resume** - Resume playback\n"
              "**!skip** - Skip current song\n"
              "**!stop** - Stop and clear queue\n"
              "**!volume** `<0-100>` - Set volume",
        inline=False
    )
    
    embed.add_field(
        name="📋 Queue & Info",
        value="**!queue** or **!q** - Show queue\n"
              "**!nowplaying** or **!np** - Current song info",
        inline=False
    )
    
    embed.add_field(
        name="🔊 Voice",
        value="**!join** - Join your voice channel\n"
              "**!leave** - Leave voice channel",
        inline=False
    )
    
    embed.set_footer(text="Powered by Spotify & YouTube with AI")
    
    await ctx.send(embed=embed)


if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("ERROR: DISCORD_TOKEN not found in environment variables!")
        print("Please create a .env file with your Discord bot token.")
        exit(1)
    
    print("Starting DiscordRecords bot...")
    bot.run(token)
