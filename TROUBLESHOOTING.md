# 🔧 Troubleshooting Guide

Common issues and their solutions for DiscordRecords.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Bot Connection Issues](#bot-connection-issues)
- [Audio Playback Issues](#audio-playback-issues)
- [API Integration Issues](#api-integration-issues)
- [Command Issues](#command-issues)
- [Performance Issues](#performance-issues)

---

## Installation Issues

### "Python not found" or "Python is not recognized"

**Problem:** Python is not installed or not in PATH.

**Solution:**
1. Download Python 3.8+ from [python.org](https://python.org)
2. During installation, check "Add Python to PATH"
3. Restart your terminal/command prompt
4. Verify: `python --version`

### "pip: command not found"

**Problem:** pip is not installed or not in PATH.

**Solution:**
```bash
# Try python -m pip instead
python -m pip install -r requirements.txt

# Or reinstall pip
python -m ensurepip --upgrade
```

### "FFmpeg not found" or "FFmpeg is not recognized"

**Problem:** FFmpeg is not installed or not in PATH.

**Solution:**

**Windows:**
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" under System Variables
   - Add new entry: `C:\ffmpeg\bin`
4. Restart terminal and verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### "No module named 'discord'"

**Problem:** Dependencies not installed.

**Solution:**
```bash
pip install -r requirements.txt

# If that fails, try:
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

---

## Bot Connection Issues

### "DISCORD_TOKEN not found in environment variables"

**Problem:** `.env` file missing or token not set.

**Solution:**
1. Ensure `.env` file exists (not `.env.example`)
2. Check file contents:
   ```
   DISCORD_TOKEN=your_actual_token_here
   ```
3. No spaces around `=`
4. Token should be a long string from Discord Developer Portal

### "Improper token has been passed"

**Problem:** Invalid Discord bot token.

**Solution:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application
3. Go to "Bot" tab
4. Click "Reset Token"
5. Copy the new token
6. Update `.env` file with new token

### Bot appears offline in Discord

**Problem:** Bot not running or connection failed.

**Solution:**
1. Check console for errors
2. Verify token is correct
3. Check internet connection
4. Ensure bot has proper intents enabled:
   - Message Content Intent
   - Server Members Intent
   - Presence Intent

### Bot doesn't respond to commands

**Problem:** Missing permissions or wrong prefix.

**Solution:**
1. Check command prefix (default: `!`)
2. Verify in `.env`: `BOT_PREFIX=!`
3. Ensure bot has "Send Messages" permission
4. Check bot role position (should be above roles it needs to interact with)
5. Try mentioning bot: `@BotName play music`

---

## Audio Playback Issues

### Bot joins but no audio plays

**Problem:** FFmpeg issue or audio configuration problem.

**Solution:**
1. Verify FFmpeg: `ffmpeg -version`
2. Check bot has "Speak" permission
3. Set volume: `!volume 50`
4. Try a different song
5. Check console for error messages

### "You need to be in a voice channel"

**Problem:** User not in voice channel or bot can't detect it.

**Solution:**
1. Join a voice channel first
2. Then use `!play` command
3. Ensure voice channel is not full
4. Check bot has "Connect" permission for that channel

### Audio cuts out or stutters

**Problem:** Network issues or CPU overload.

**Solution:**
1. Check internet connection speed
2. Try lower volume: `!volume 30`
3. Close other applications
4. Choose a different music source
5. Restart the bot

### "Failed to play audio" error

**Problem:** yt-dlp or FFmpeg issue.

**Solution:**
```bash
# Update yt-dlp
pip install --upgrade yt-dlp

# Reinstall FFmpeg
# Windows: Download fresh copy
# macOS: brew reinstall ffmpeg
# Linux: sudo apt install --reinstall ffmpeg
```

### Bot plays but volume is very low

**Problem:** Volume setting too low.

**Solution:**
```
!volume 100
```

Also check:
- Discord user volume slider
- System volume
- Voice channel volume settings

---

## API Integration Issues

### Spotify features not working

**Problem:** Invalid credentials or API issue.

**Solution:**
1. Verify credentials in `.env`:
   ```
   SPOTIFY_CLIENT_ID=your_id
   SPOTIFY_CLIENT_SECRET=your_secret
   ```
2. Check credentials at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
3. Ensure both ID and Secret are from the same app
4. Look for errors in console
5. Bot will fall back to YouTube if Spotify fails

### "AI language processing not enabled"

**Problem:** Anthropic API key not set or invalid.

**Solution:**
1. This is optional - bot still works with keyword matching
2. To enable AI:
   - Get key from [Anthropic Console](https://console.anthropic.com/)
   - Add to `.env`: `ANTHROPIC_API_KEY=your_key`
   - Restart bot
3. Check console for "✅ AI language processing enabled"

### YouTube search returns no results

**Problem:** yt-dlp issue or search query problem.

**Solution:**
```bash
# Update yt-dlp
pip install --upgrade yt-dlp

# Try a direct YouTube URL instead
!play https://youtube.com/watch?v=...
```

### Rate limiting errors

**Problem:** Too many API requests.

**Solution:**
1. Wait a few minutes
2. Use less frequent commands
3. For Spotify: Check your API quota in developer dashboard
4. Consider implementing caching (future feature)

---

## Command Issues

### "Command not found"

**Problem:** Wrong command name or prefix.

**Solution:**
1. Check available commands: `!help_music`
2. Verify prefix: `!` (default)
3. Try aliases: `!p` instead of `!play`

### Queue doesn't show anything

**Problem:** No songs in queue or empty queue.

**Solution:**
1. Add songs first: `!play some music`
2. Wait for songs to download
3. Check current song: `!nowplaying`

### Skip command doesn't work

**Problem:** Nothing playing or already at end of queue.

**Solution:**
1. Check if music is playing: `!nowplaying`
2. Ensure queue has songs: `!queue`
3. Use `!play` to add more songs

---

## Performance Issues

### Bot uses too much CPU

**Problem:** FFmpeg or Python process consuming resources.

**Solution:**
1. Lower audio quality (modify ytdl_options in player.py)
2. Limit queue size
3. Restart bot regularly
4. Use a dedicated server/VPS for 24/7 hosting

### Bot memory usage increases over time

**Problem:** Memory leak or queue buildup.

**Solution:**
1. Restart bot periodically
2. Clear queue: `!stop`
3. Limit maximum queue size in config
4. Update to latest version

### Slow command response

**Problem:** Network latency or API delays.

**Solution:**
1. Check internet connection
2. Use faster hosting (VPS instead of home computer)
3. Consider geographic proximity to Discord servers
4. Enable caching (future feature)

---

## Advanced Debugging

### Enable Debug Logging

Add to bot.py:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Dependencies

```bash
pip list | grep -E "discord|spotipy|yt-dlp|anthropic"
```

### Test Individual Components

```python
# Test Spotify
python -c "from services.spotify_service import SpotifyService; s = SpotifyService(); print(s.enabled)"

# Test YouTube
python -c "from services.youtube_service import YouTubeService; y = YouTubeService()"
```

### Common Error Codes

| Error | Meaning | Solution |
|-------|---------|----------|
| 401 | Unauthorized | Check API credentials |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Invalid URL or ID |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Try again later |

---

## Still Need Help?

1. **Check console output** - Most errors are logged there
2. **Read error messages carefully** - They often tell you what's wrong
3. **Search existing issues** on GitHub
4. **Create a new issue** with:
   - Your OS and Python version
   - Complete error message
   - Steps to reproduce
   - What you've already tried

## Quick Diagnostics Checklist

Run through this list:
- [ ] Python 3.8+ installed? (`python --version`)
- [ ] FFmpeg installed? (`ffmpeg -version`)
- [ ] Dependencies installed? (`pip list`)
- [ ] `.env` file exists and has valid token?
- [ ] Bot is online in Discord?
- [ ] Bot has proper permissions?
- [ ] You're in a voice channel?
- [ ] Internet connection working?
- [ ] Console shows errors?

---

**Most issues can be solved by:**
1. Checking the console output
2. Verifying all credentials
3. Ensuring FFmpeg is installed
4. Updating dependencies: `pip install --upgrade -r requirements.txt`
