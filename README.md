# 🎵 DiscordRecords

An AI-powered Discord music bot that understands natural language requests and plays music from Spotify and YouTube.

## ✨ Features

- 🤖 **AI-Powered Natural Language Understanding**: Ask for music in plain English!
  - "Play some DnD tavern music"
  - "I want chill lo-fi beats for studying"
  - "Queue up a rock workout playlist"

- 🎵 **Multi-Source Support**:
  - YouTube search and direct playback (no credentials needed)
  - Spotify playlist and track search (optional, free API)

- 🎛️ **Full Playback Controls**:
  - Queue management with playlist support
  - Play, pause, resume, skip
  - Volume control
  - Now playing info

- 🧠 **Smart Music Discovery**:
  - Understands moods, genres, and activities
  - Searches playlists by name on Spotify or YouTube
  - Falls back to keyword matching if AI is unavailable

## 📋 Requirements

### Required (Free)
- Python 3.8 or higher
- Discord Bot Token (free from Discord Developer Portal)

### Bundled
- **FFmpeg** — included in the repo (`ffmpeg.exe`), no separate install needed

### Optional Enhancements
- **Spotify API credentials** (FREE — enables Spotify search/playlists)
- **OpenAI or Anthropic API key** (PAID ~$3–15/month — enables advanced AI understanding)
  - The bot works great WITHOUT AI using keyword matching!

## 🚀 Getting Started

### 1. Create a Discord Bot (one-time)

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** → name it → go to the **Bot** tab
3. Click **Reset Token** → copy it (you'll paste it during setup)https://www.youtube.com/watch?v=vGfJeW_CcFY
4. Enable **Message Content Intent**, **Server Members Intent**, and **Presence Intent**
5. Go to **OAuth2 → URL Generator**, select scopes `bot` + `applications.commands`, permissions: Send Messages, Connect, Speak
6. Open the generated URL to invite the bot to your server

### 2. Run Setup

```bash
git clone https://github.com/yourusername/DiscordRecords.git
cd DiscordRecords
python setup.py
```

The wizard handles everything: checks Python, verifies FFmpeg, installs dependencies, and prompts for your Discord token (plus optional Spotify/AI keys).

### 3. Start the Bot

```bash
python bot.py
```

Join a voice channel and type `!play lofi hip hop` — that's it.

## 🎮 Commands

### Music Playback

| Command | Aliases | Description | Example |
|---------|---------|-------------|---------|
| `!play <query>` | `!p` | Play music using natural language | `!play DnD tavern music` |
| `!background <theme>` | `!bg` | Set background music (lower priority) | `!background chill lofi` |
| `!background stop` | — | Stop background music | `!background stop` |
| `!pause` | — | Pause current playback | `!pause` |
| `!resume` | — | Resume paused playback | `!resume` |
| `!skip` | `!next` | Skip to next song | `!skip` |
| `!stop` | — | Stop playback and clear queue | `!stop` |
| `!volume <0-100>` | `!vol` | Set volume | `!volume 50` |

### Queue Management

| Command | Aliases | Description |
|---------|---------|-------------|
| `!queue` | `!q` | Show current queue |
| `!nowplaying` | `!np`, `!current` | Show current song info |

### Voice Channel

| Command | Aliases | Description |
|---------|---------|-------------|
| `!join` | — | Join your voice channel |
| `!leave` | `!disconnect`, `!dc` | Leave voice channel |

### Help

| Command | Aliases | Description |
|---------|---------|-------------|
| `!help_music` | `!musichelp` | Show detailed command help |

## 💡 Example Usage

```
User: !play some epic fantasy battle music
Bot: 🤖 Understanding your request...
     🎵 Searching for: Epic fantasy orchestral battle music
     ✅ Now playing: Epic Battle Music - Two Steps From Hell

User: !play a chill lofi playlist
Bot: 🔍 Searching Spotify playlists for: chill lofi
     📋 Found playlist: Lofi Beats (50 tracks)
     ✅ Added 20 songs to the queue!

User: !play Shape of You
Bot: 🔍 Searching Spotify for: Shape of You Ed Sheeran
     ✅ Now playing: Ed Sheeran - Shape of You
```

## 📁 Project Structure

```
DiscordRecords/
├── bot.py                    # Main bot entry point
├── setup.py                  # Install wizard (run this first)
├── config.json.example       # Configuration template
├── requirements.txt          # Python dependencies
├── ffmpeg.exe                # Bundled audio encoder
├── ffplay.exe                # Bundled audio player
├── ffprobe.exe               # Bundled audio probe
│
├── ai/
│   └── language_processor.py # Natural language understanding
│
├── music/
│   └── player.py             # Music player and queue management
│
└── services/
    ├── spotify_service.py    # Spotify API wrapper
    └── youtube_service.py    # YouTube search wrapper
```

## 🔧 Configuration

All configuration lives in `config.json` (created by `setup.py`):

```json
{
    "discord_token": "your_token",
    "bot_prefix": "!",
    "spotify": {
        "client_id": "",
        "client_secret": ""
    },
    "openai": {
        "api_key": ""
    },
    "anthropic": {
        "api_key": ""
    },
    "bot_settings": {
        "default_volume": 50,
        "max_queue_size": 100,
        "timeout_seconds": 300,
        "enable_auto_disconnect": true
    }
}
```

### Without AI (Basic Mode)
If no Anthropic or OpenAI API key is provided, the bot uses keyword-based matching — still works great for most requests.

### Without Spotify
If no Spotify credentials are provided, the bot uses YouTube exclusively — still fully functional.

## 🔒 Security

`config.json` contains secrets and is git-ignored. Never commit it.

If you accidentally expose a token:
1. Discord: Developer Portal → Bot → Reset Token
2. Spotify: Delete the app, create a new one
3. Anthropic: Revoke the key in console

## 🐛 Troubleshooting

See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for common issues.

## 🤝 Contributing

Contributions are welcome! See **[CONTRIBUTING.md](CONTRIBUTING.md)**.

## 📝 License

MIT License

## 🙏 Acknowledgments

- [discord.py](https://discordpy.readthedocs.io/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Spotipy](https://spotipy.readthedocs.io/)
- [Anthropic Claude](https://www.anthropic.com/)