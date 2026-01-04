# 🎵 DiscordRecords

An AI-powered Discord music bot that understands natural language requests and plays music from Spotify and YouTube.

## ✨ Features

- 🤖 **AI-Powered Natural Language Understanding**: Ask for music in plain English!
  - "Play some DnD tavern music"
  - "I want chill lo-fi beats for studying"
  - "Play Bohemian Rhapsody"
  
- 🎵 **Multi-Source Support**:
  - YouTube integration for direct playback
  - Spotify integration for playlists and recommendations
  
- 🎛️ **Full Playback Controls**:
  - Queue management
  - Play, pause, resume, skip
  - Volume control
  - Now playing info
  
- 🧠 **Smart Music Discovery**:
  - Understands moods, genres, and activities
  - Can interpret vague requests
  - Falls back to keyword matching if AI is unavailable

## 📋 Requirements

### Required (Free)
- Python 3.8 or higher
- FFmpeg (for audio processing)
- Discord Bot Token (free from Discord Developer Portal)

### Optional Enhancements
- **Spotify API credentials** (FREE - enables Spotify search/playlists)
- **Anthropic API key** (PAID ~$3-15/month - enables advanced AI understanding)
  - ⚠️ **Note**: The bot works great WITHOUT AI using keyword matching!
  - Only get this if you want advanced natural language processing

## 🚀 Quick Start

### 1. Install FFmpeg

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add to PATH or place in the project directory

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 2. Clone and Setup

```bash
git clone https://github.com/yourusername/DiscordRecords.git
cd DiscordRecords
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
DISCORD_TOKEN=your_discord_bot_token_here
BOT_PREFIX=!
SPOTIFY_CLIENT_ID=your_spotify_client_id_here  # Optional
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here  # Optional
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Optional
```

### 4. Get API Credentials

#### Discord Bot Token (Required)
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a New Application
3. Go to the "Bot" section
4. Click "Reset Token" and copy your token
5. Enable these Privileged Gateway Intents:
   - Message Content Intent
   - Server Members Intent
6. Go to OAuth2 > URL Generator
7. Select scopes: `bot`, `applications.commands`
8. Select bot permissions: 
   - Send Messages
   - Connect
   - Speak
   - Use Voice Activity
9. Copy and visit the generated URL to invite the bot

#### Spotify API (Optional - FREE)
**Cost**: Free forever for developers

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account (free account works)
3. Click "Create App"
4. Fill in:
   - App name: `DiscordRecords` (or any name)
   - App description: `Discord music bot`
   - Redirect URI: `http://localhost:8888/callback` (required but not used)
5. Accept terms and click "Create"
6. Click "Settings" on your new app
7. Copy the **Client ID** and **Client Secret** (click "View client secret")
8. Add to your `.env` file:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   ```

**What you get with Spotify**:
- Search Spotify's catalog
- Import Spotify playlists
- Better music metadata
- Track recommendations

**Without Spotify**: Bot uses YouTube only (still fully functional!)

#### Anthropic API (Optional - PAID)
**Cost**: ~$3-15 per month depending on usage

⚠️ **Important**: This is NOT required! The bot has excellent keyword matching built-in.

Only get this if you want cutting-edge AI understanding of vague requests.

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an account
3. Add credits to your account ($5 minimum)
4. Create an API key
5. Add to `.env`: `ANTHROPIC_API_KEY=your_key_here`

**With AI**: Understands complex requests like "play something epic for a boss fight"
**Without AI**: Uses keyword matching - still handles most requests perfectly!

### 5. Run the Bot

```bash
python bot.py
```

## 🎮 Commands

### Music Playback

| Command | Aliases | Description | Example |
|---------|---------|-------------|---------|
| `!play <query>` | `!p` | Play music based on natural language | `!play DnD tavern music` |
| `!pause` | - | Pause current playback | `!pause` |
| `!resume` | - | Resume paused playback | `!resume` |
| `!skip` | `!next` | Skip to next song | `!skip` |
| `!stop` | - | Stop playback and clear queue | `!stop` |
| `!volume <0-100>` | `!vol` | Set volume | `!volume 50` |

### Queue Management

| Command | Aliases | Description |
|---------|---------|-------------|
| `!queue` | `!q` | Show current queue |
| `!nowplaying` | `!np`, `!current` | Show current song info |

### Voice Channel

| Command | Aliases | Description |
|---------|---------|-------------|
| `!join` | - | Join your voice channel |
| `!leave` | `!disconnect`, `!dc` | Leave voice channel |

### Help

| Command | Aliases | Description |
|---------|---------|-------------|
| `!help_music` | `!musichelp` | Show detailed command help |

## 💡 Example Usage

```
User: !play some epic fantasy battle music
Bot: 🤖 Understanding your request: 'some epic fantasy battle music'...
     🎵 Searching for: Epic fantasy orchestral battle music
     🔍 Type: genre
     ✅ Now playing: Epic Battle Music - Two Steps From Hell

User: !play Shape of You
Bot: 🤖 Understanding your request: 'Shape of You'...
     🎵 Searching for: Shape of You Ed Sheeran
     🔍 Type: search
     ✅ Now playing: Ed Sheeran - Shape of You (Official Music Video)

User: !play chill lo-fi beats for studying
Bot: 🤖 Understanding your request: 'chill lo-fi beats for studying'...
     🎵 Searching for: Lofi hip hop chill study beats
     🔍 Type: mood
     ✅ Added 20 songs to the queue!
```

## 📁 Project Structure

```
DiscordRecords/
├── bot.py                          # Main bot file
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── config.json.example             # Configuration template
├── README.md                       # This file
│
├── ai/                            # AI/Language processing
│   ├── __init__.py
│   └── language_processor.py      # Natural language understanding
│
├── music/                         # Music playback
│   ├── __init__.py
│   └── player.py                  # Music player and queue management
│
└── services/                      # External API integrations
    ├── __init__.py
    ├── spotify_service.py         # Spotify API wrapper
    └── youtube_service.py         # YouTube search wrapper
```

## 🔧 Advanced Configuration

### Without AI (Basic Mode)

If you don't provide an Anthropic API key, the bot will use keyword-based matching:
- Still works great for straightforward requests
- Recognizes genres, moods, and activities
- Falls back to simple YouTube search

### Without Spotify

If you don't provide Spotify credentials:
- Bot will use YouTube exclusively
- All searches go directly to YouTube
- Still fully functional for most use cases

### Customization

Edit `config.json` (copy from `config.json.example`) to customize:
- Default volume level
- Maximum queue size
- Auto-disconnect timeout
- Other bot behaviors

## � Security & Secrets Management

### ⚠️ NEVER Commit Secrets to Git

Your `.env` file contains sensitive information and is automatically git-ignored.

**What to keep private**:
- Discord bot tokens
- Spotify API credentials  
- Anthropic API keys
- Any other API keys

### For Repository Collaborators

If multiple people need to run the bot:

1. **Each person creates their own Discord bot** at [Discord Developer Portal](https://discord.com/developers/applications)
2. **Each person creates their own `.env` file** with their credentials
3. **Share only**: `.env.example` (template) and documentation

### For Deployment (24/7 Hosting)

If deploying to a server (Heroku, AWS, VPS, etc.):

1. **Use environment variables** on the hosting platform
2. **Never commit** your production `.env` file
3. Common platforms:
   - **Heroku**: Use Config Vars in dashboard
   - **AWS/DigitalOcean**: Set environment variables in deployment config
   - **Docker**: Use docker-compose environment variables
   - **VPS**: Copy `.env` file directly via SSH (not git)

### Rotating Compromised Keys

If you accidentally commit a token:

1. **Immediately** go to Discord Developer Portal → Bot → Reset Token
2. For Spotify: Delete the app and create a new one
3. For Anthropic: Revoke the key in the console
4. Update your `.env` with new credentials
5. Remove from git history: `git filter-branch` or use [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
## 🎨 Customizing Your Bot

### Change Bot Name and Avatar

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application
3. In "General Information":
   - Change the name (e.g., "Green-bot", "DJ Bot", etc.)
   - Upload a custom avatar image
4. Changes appear in Discord within a few minutes

### Change Command Prefix

Edit your `.env` file:
```
BOT_PREFIX=?
# Now commands are: ?play, ?pause, etc.
```

Or use any prefix you want: `$`, `>`, `green!`, etc.

### Change Bot Status

Edit [bot.py](bot.py) in the `on_ready` function:
```python
await bot.change_presence(
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="your custom status here"  # Change this!
    )
)
```

Status types:
- `ActivityType.playing` - "Playing ..."
- `ActivityType.listening` - "Listening to ..."
- `ActivityType.watching` - "Watching ..."
- `ActivityType.streaming` - Shows as streaming

### Customize Responses

Edit messages in [bot.py](bot.py) to match your bot's personality:
```python
# Find lines like:
await ctx.send("✅ Now playing!")
# Change to:
await ctx.send("🎵 Vibing to:")
```

## 🚀 24/7 Hosting & Deployment

Want your bot online 24/7 without keeping your computer on?

See the complete **[DEPLOYMENT.md](DEPLOYMENT.md)** guide for:
- Free hosting options (Oracle Cloud, Railway, Replit)
- VPS setup ($5/month)
- Running on Linux with systemd
- Windows auto-start
- Docker deployment
- Cost comparisons

**Quick option**: Run on your home computer with the auto-start scripts!
## �🐛 Troubleshooting

### Bot doesn't join voice channel
- Ensure the bot has "Connect" and "Speak" permissions
- Check that you're in a voice channel when using `!play`

### No sound/Audio issues
- Verify FFmpeg is installed and in PATH
- Check bot's volume with `!volume`
- Ensure the bot has "Speak" permission

### Spotify features not working
- Verify your Spotify credentials in `.env`
- Ensure credentials are from the same Spotify Developer app
- Check console logs for Spotify-related errors

### AI understanding not working
- Verify your Anthropic API key is correct
- Bot will automatically fall back to keyword matching
- Check console for "AI language processing enabled" message

### Import errors
- Run `pip install -r requirements.txt` again
- Ensure you're using Python 3.8+
- Try creating a fresh virtual environment

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [discord.py](https://discordpy.readthedocs.io/)
- Uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube integration
- Uses [Spotipy](https://spotipy.readthedocs.io/) for Spotify integration
- Uses [Anthropic Claude](https://www.anthropic.com/) for AI understanding

## 📞 Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section above
2. Review existing GitHub issues
3. Create a new issue with details about your problem

---

## 🔗 Additional Resources

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - 24/7 hosting options and setup
- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 10 minutes
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - How the bot works internally
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Fix common issues
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Help improve the bot

---

**Note**: This bot is for personal/educational use. Respect copyright laws and platform terms of service when using this bot.

**Cost Summary**:
- ✅ FREE: Discord bot + YouTube + Spotify API
- 💵 OPTIONAL: Anthropic AI ($3-15/month) - bot works great without it!
- 💻 OPTIONAL: VPS hosting ($0-10/month) - or run on your own computer
