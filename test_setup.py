"""
Quick test script to verify the bot setup before deploying to Discord
"""
import sys

print("=" * 60)
print("  DiscordRecords Setup Test")
print("=" * 60)
print()

# Test 1: Python version
print("✓ Python version:", sys.version.split()[0])

# Test 2: Import discord.py
try:
    import discord
    print("✓ discord.py imported successfully")
except ImportError as e:
    print("✗ Failed to import discord.py:", e)
    sys.exit(1)

# Test 3: Import yt-dlp
try:
    import yt_dlp
    print("✓ yt-dlp imported successfully")
except ImportError as e:
    print("✗ Failed to import yt-dlp:", e)
    sys.exit(1)

# Test 4: Import dotenv
try:
    from dotenv import load_dotenv
    print("✓ python-dotenv imported successfully")
except ImportError as e:
    print("✗ Failed to import python-dotenv:", e)
    sys.exit(1)

# Test 5: Check .env file
import os
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
if discord_token and discord_token != 'your_discord_bot_token_here':
    print("✓ Discord token found in .env")
else:
    print("⚠ Discord token not set in .env (need to add your token)")

# Test 6: Optional integrations
spotify_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
if spotify_id and spotify_id != 'your_spotify_client_id_here':
    print("✓ Spotify credentials found")
else:
    print("⚠ Spotify credentials not set (optional - will use YouTube only)")

anthropic_key = os.getenv('ANTHROPIC_API_KEY')
if anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
    print("✓ Anthropic API key found")
else:
    print("⚠ Anthropic API key not set (optional - will use keyword matching)")

# Test 7: Check FFmpeg
import shutil
if shutil.which("ffmpeg"):
    print("✓ FFmpeg is installed and in PATH")
else:
    print("✗ FFmpeg NOT FOUND - Required for audio playback!")
    print("  Download from: https://ffmpeg.org/download.html")
    print("  For Windows: Add ffmpeg.exe to PATH or place in project folder")

# Test 8: Test bot modules
try:
    from music.player import MusicPlayer
    print("✓ Music player module loads successfully")
except Exception as e:
    print("✗ Failed to load music player:", e)

try:
    from services.spotify_service import SpotifyService
    print("✓ Spotify service module loads successfully")
except Exception as e:
    print("✗ Failed to load Spotify service:", e)

try:
    from services.youtube_service import YouTubeService
    print("✓ YouTube service module loads successfully")
except Exception as e:
    print("✗ Failed to load YouTube service:", e)

try:
    from ai.language_processor import LanguageProcessor
    print("✓ AI language processor module loads successfully")
except Exception as e:
    print("✗ Failed to load language processor:", e)

print()
print("=" * 60)
print("  Summary")
print("=" * 60)

if not shutil.which("ffmpeg"):
    print()
    print("⚠ ACTION REQUIRED: Install FFmpeg before running the bot!")
    print("   Without FFmpeg, audio will NOT work.")
    print()
    print("   Download: https://ffmpeg.org/download.html")
    print("   Windows Quick Fix: Download and place ffmpeg.exe in this folder")
    print()

if not discord_token or discord_token == 'your_discord_bot_token_here':
    print()
    print("⚠ ACTION REQUIRED: Add your Discord bot token to .env file!")
    print("   Get it from: https://discord.com/developers/applications")
    print()
else:
    print()
    print("✓ Ready to run! (Except FFmpeg if not installed)")
    print()
    print("To start the bot:")
    print("  python bot.py")
    print()
