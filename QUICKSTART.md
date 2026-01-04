# 🚀 Quick Start Guide

This guide will get your DiscordRecords bot up and running in under 10 minutes!

## Prerequisites

- Python 3.8+ installed
- A Discord account
- (Optional) Spotify Developer account
- (Optional) Anthropic API account

## Step 1: Install FFmpeg

FFmpeg is required for audio processing.

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract and add to your PATH, or place `ffmpeg.exe` in the project folder

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update && sudo apt install ffmpeg
```

## Step 2: Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give it a name (e.g., "DiscordRecords")
4. Go to the "Bot" tab
5. Click "Reset Token" and **copy your token** (you'll need this!)
6. Enable these intents:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
   - ✅ Presence Intent

## Step 3: Invite Bot to Your Server

1. Still in Developer Portal, go to OAuth2 > URL Generator
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select permissions:
   - ✅ Send Messages
   - ✅ Connect
   - ✅ Speak
   - ✅ Use Voice Activity
   - ✅ Read Message History
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

## Step 4: Setup the Bot

**Option A: Automated Setup (Recommended)**
```bash
python setup.py
```
Follow the prompts to configure your bot.

**Option B: Manual Setup**
```bash
# Copy environment file
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Edit .env and add your Discord token
# You can use any text editor
```

## Step 5: Run the Bot

**Windows:**
```bash
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

**Or directly with Python:**
```bash
python bot.py
```

## Step 6: Test It!

1. Join a voice channel in your Discord server
2. Type: `!play lofi hip hop`
3. Enjoy your music! 🎵

## Common First-Time Issues

### "DISCORD_TOKEN not found"
- Make sure you created a `.env` file (not `.env.example`)
- Ensure your token is on the line `DISCORD_TOKEN=your_token_here`
- No spaces around the `=` sign

### "Bot doesn't join voice channel"
- Make sure you're in a voice channel
- Check bot permissions in Discord server settings
- Ensure bot has "Connect" and "Speak" permissions

### "No audio playing"
- Verify FFmpeg is installed: run `ffmpeg -version`
- Check bot volume: `!volume 50`
- Try a different song

## Optional: Enable Advanced Features

### Spotify Integration
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create an app
3. Copy Client ID and Client Secret
4. Add to `.env`:
   ```
   SPOTIFY_CLIENT_ID=your_id
   SPOTIFY_CLIENT_SECRET=your_secret
   ```

### AI Language Understanding
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. Add to `.env`:
   ```
   ANTHROPIC_API_KEY=your_key
   ```

## Next Steps

- Read the full [README.md](README.md) for all commands
- Join a voice channel and try: `!play DnD tavern music`
- Experiment with natural language requests
- Customize bot prefix in `.env`

## Getting Help

If something doesn't work:
1. Check the error message in the console
2. Read the [Troubleshooting](README.md#-troubleshooting) section
3. Make sure all prerequisites are installed
4. Try running `setup.py` again

---

**Need more help?** Check the full documentation in [README.md](README.md)
