#!/usr/bin/env python3
"""
Setup script for DiscordRecords bot
Installs dependencies and creates config.json
"""
import json
import os
import sys
import subprocess


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False

    print("✅ Python version is compatible")
    return True


def check_ffmpeg():
    """Check if bundled FFmpeg is present"""
    print_header("Checking FFmpeg")

    ffmpeg_path = os.path.join(SCRIPT_DIR, 'ffmpeg.exe')
    if os.path.exists(ffmpeg_path):
        print("✅ FFmpeg is bundled in project")
        return True
    else:
        print("⚠️  ffmpeg.exe not found in project folder")
        print("  The bot expects ffmpeg.exe in the repo root.")
        return False

def check_deno():
    """Check if Deno JavaScript runtime is installed (required by yt-dlp)"""
    print_header("Checking Deno (JavaScript Runtime)")

    try:
        result = subprocess.run(['deno', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.strip().split('\n')[0]
            print(f"\u2705 Deno is installed ({version_line})")
            return True
    except FileNotFoundError:
        pass

    print("\u26a0\ufe0f  Deno is not installed")
    print("  yt-dlp requires Deno to extract YouTube videos.")
    print("  Install it with: winget install DenoLand.Deno")
    print("  Or visit: https://deno.land/")
    print("  After installing, restart your terminal.")
    return False

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Python Dependencies")

    req_path = os.path.join(SCRIPT_DIR, 'requirements.txt')
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
        print("\n✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Failed to install dependencies")
        return False


def setup_config():
    """Create config.json interactively"""
    print_header("Bot Configuration")

    config_path = os.path.join(SCRIPT_DIR, 'config.json')

    if os.path.exists(config_path):
        print("⚠️  config.json already exists")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("Skipping config setup")
            return True

    # Discord token (required)
    print("You need a Discord Bot Token.")
    print("Get one at: https://discord.com/developers/applications")
    print("  1. Create an Application")
    print("  2. Go to the Bot tab, click Reset Token, copy it")
    discord_token = input("\nPaste your Discord Bot Token (required): ").strip()

    if not discord_token:
        print("⚠️  No token provided - you'll need to add it to config.json manually")

    # Spotify (optional)
    print("\n" + "-"*60)
    print("Optional: Spotify Integration")
    print("-"*60)
    print("Lets the bot resolve Spotify links and search playlists.")
    print("Requires a free Spotify Developer app (not a user account).")
    print("Get credentials at: https://developer.spotify.com/dashboard")

    spotify_id = ""
    spotify_secret = ""
    setup_spotify = input("\nSetup Spotify? (y/N): ").strip().lower()
    if setup_spotify == 'y':
        spotify_id = input("Spotify Client ID: ").strip()
        spotify_secret = input("Spotify Client Secret: ").strip()
        if spotify_id and spotify_secret:
            print("✅ Spotify credentials configured")

    # AI (optional - OpenAI or Anthropic)
    print("\n" + "-"*60)
    print("Optional: AI Language Understanding")
    print("-"*60)
    print("Enables natural language interpretation of music requests.")
    print("Supports OpenAI or Anthropic (pick one).")
    print("  OpenAI:    https://platform.openai.com/api-keys")
    print("  Anthropic: https://console.anthropic.com/")

    openai_key = ""
    anthropic_key = ""
    setup_ai = input("\nSetup AI? (y/N): ").strip().lower()
    if setup_ai == 'y':
        print("  1) OpenAI")
        print("  2) Anthropic")
        ai_choice = input("Which provider? (1/2): ").strip()
        if ai_choice == '1':
            openai_key = input("OpenAI API Key: ").strip()
            if openai_key:
                print("✅ OpenAI API key configured")
        else:
            anthropic_key = input("Anthropic API Key: ").strip()
            if anthropic_key:
                print("✅ Anthropic API key configured")

    # Write config
    config = {
        "discord_token": discord_token,
        "bot_prefix": "!",
        "spotify": {
            "client_id": spotify_id,
            "client_secret": spotify_secret
        },
        "openai": {
            "api_key": openai_key
        },
        "anthropic": {
            "api_key": anthropic_key
        },
        "bot_settings": {
            "default_volume": 50,
            "max_queue_size": 100,
            "timeout_seconds": 300,
            "enable_auto_disconnect": True
        }
    }

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

    print("\n✅ config.json created")
    return True


def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete!")

    print("Next steps:")
    print("1. Invite your bot to your Discord server:")
    print("   - Go to Discord Developer Portal")
    print("   - Select your application > OAuth2 > URL Generator")
    print("   - Scopes: bot, applications.commands")
    print("   - Permissions: Send Messages, Connect, Speak")
    print("   - Open the generated URL and authorize")
    print("2. Run the bot:")
    print("   python bot.py")
    print("\n🎵 Happy listening! 🎵\n")


def main():
    """Main setup function"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║            🎵 DiscordRecords Setup Wizard 🎵              ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")

    if not check_python_version():
        sys.exit(1)

    check_ffmpeg()
    check_deno()

    if not install_dependencies():
        sys.exit(1)

    if not setup_config():
        sys.exit(1)

    print_next_steps()


if __name__ == '__main__':
    main()


if __name__ == "__main__":
    main()
