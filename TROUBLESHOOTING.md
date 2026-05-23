# 🔧 Troubleshooting Guide

Common issues and solutions for DiscordRecords.

---

## Installation Issues

### "Python not found"

Python is not installed or not in PATH.

1. Download Python 3.8+ from [python.org](https://python.org)
2. During install, check **"Add Python to PATH"**
3. Restart your terminal
4. Verify: `python --version`

### "pip: command not found"

```bash
python -m pip install -r requirements.txt
```

### "No module named 'discord'" (or other import errors)

Dependencies not installed. Run setup again:
```bash
python setup.py
```

Or manually:
```bash
pip install -r requirements.txt
```

---

## Bot Connection Issues

### "DISCORD_TOKEN not found" or bot won't start

`config.json` is missing or the token field is empty.

1. Run `python setup.py` to create it
2. Or manually edit `config.json` and paste your token in the `discord_token` field

### "Improper token has been passed"

Your token is invalid or expired.

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your app → Bot tab → **Reset Token**
3. Copy the new token into `config.json`

### Bot appears offline in Discord

1. Make sure `python bot.py` is running without errors in the console
2. Verify you enabled these intents in the Developer Portal:
   - Message Content Intent
   - Server Members Intent
   - Presence Intent

### Bot doesn't respond to commands

1. Check the prefix — default is `!` (set in `config.json` under `bot_prefix`)
2. Ensure the bot has **Send Messages** permission in the channel
3. Try `!help_music` to confirm it's alive

---

## Audio Playback Issues

### Bot joins voice channel but no audio plays

1. Check bot has **Speak** permission in the voice channel
2. Try `!volume 50` to make sure volume isn't at zero
3. Check the console for error messages
4. Verify `ffmpeg.exe` exists in the project root folder

### "You need to be in a voice channel"

You must join a voice channel first, then type `!play`.

### Audio cuts out or stutters

1. Check your internet connection
2. Try a different song
3. Restart the bot (`Ctrl+C`, then `python bot.py` again)

### "Failed to play audio" or FFmpeg errors

```bash
# Update yt-dlp (YouTube changes frequently)
pip install --upgrade yt-dlp
```

Also confirm `ffmpeg.exe` is in the project root (it should be bundled with the repo).

---

## Spotify Issues

### "Spotify credentials not found - Spotify features disabled"

This is normal if you skipped Spotify setup. The bot works fine with YouTube only.

To enable Spotify:
1. Get credentials at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Edit `config.json` and fill in `spotify.client_id` and `spotify.client_secret`
3. Restart the bot

### Spotify playlist not found

1. Make sure both Client ID and Secret are from the same app
2. Check the console for specific error messages
3. The bot will fall back to YouTube if Spotify fails

---

## AI / Language Processing Issues

### "No AI API key found - Using basic keyword matching"

This is normal if you skipped AI setup. The bot uses keyword matching instead — still works for most requests.

To enable AI (pick one provider):

**OpenAI:**
1. Get a key at [OpenAI Platform](https://platform.openai.com/api-keys)
2. Edit `config.json` and fill in `openai.api_key`
3. Restart the bot

**Anthropic:**
1. Get a key at [Anthropic Console](https://console.anthropic.com/)
2. Edit `config.json` and fill in `anthropic.api_key`
3. Restart the bot

---

## Quick Diagnostics Checklist

- [ ] Python 3.8+? (`python --version`)
- [ ] `config.json` exists with a valid Discord token?
- [ ] `ffmpeg.exe` in project folder?
- [ ] Dependencies installed? (`pip list | findstr discord`)
- [ ] Bot intents enabled in Developer Portal?
- [ ] Bot has Send Messages + Connect + Speak permissions?
- [ ] You're in a voice channel when using `!play`?

---

## Still Stuck?

1. Check the console output — most errors are logged there
2. Search existing GitHub issues
3. Create a new issue with: your OS, Python version, the full error message, and what you tried
