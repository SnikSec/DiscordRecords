#!/usr/bin/env python3
"""
Setup script for DiscordRecords bot
Helps with initial configuration and dependency checking
"""
import os
import sys
import subprocess
import shutil


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
    """Check if FFmpeg is installed"""
    print_header("Checking FFmpeg Installation")
    
    if shutil.which("ffmpeg") is not None:
        print("✅ FFmpeg is installed")
        return True
    else:
        print("⚠️  FFmpeg is not installed or not in PATH")
        print("\nFFmpeg is required for audio playback.")
        print("Please install it:")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        print("  macOS: brew install ffmpeg")
        print("  Linux: sudo apt install ffmpeg")
        return False


def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Python Dependencies")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Failed to install dependencies")
        return False


def setup_env_file():
    """Setup .env file from example"""
    print_header("Setting up Environment File")
    
    if os.path.exists(".env"):
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("Skipping .env setup")
            return True
    
    if not os.path.exists(".env.example"):
        print("❌ .env.example not found!")
        return False
    
    # Copy example file
    shutil.copy(".env.example", ".env")
    print("✅ Created .env file from template")
    
    # Ask for Discord token
    print("\n" + "-"*60)
    print("Let's configure your bot!")
    print("-"*60)
    
    discord_token = input("\nEnter your Discord Bot Token (required): ").strip()
    if discord_token:
        with open(".env", "r") as f:
            content = f.read()
        content = content.replace("your_discord_bot_token_here", discord_token)
        with open(".env", "w") as f:
            f.write(content)
        print("✅ Discord token configured")
    else:
        print("⚠️  No Discord token provided - you'll need to add it manually")
    
    # Ask about optional features
    print("\n" + "-"*60)
    print("Optional Features")
    print("-"*60)
    
    setup_spotify = input("\nDo you want to setup Spotify integration? (y/N): ").strip().lower()
    if setup_spotify == 'y':
        client_id = input("Spotify Client ID: ").strip()
        client_secret = input("Spotify Client Secret: ").strip()
        
        if client_id and client_secret:
            with open(".env", "r") as f:
                content = f.read()
            content = content.replace("your_spotify_client_id_here", client_id)
            content = content.replace("your_spotify_client_secret_here", client_secret)
            with open(".env", "w") as f:
                f.write(content)
            print("✅ Spotify credentials configured")
    
    setup_ai = input("\nDo you want to setup AI language understanding? (y/N): ").strip().lower()
    if setup_ai == 'y':
        api_key = input("Anthropic API Key: ").strip()
        
        if api_key:
            with open(".env", "r") as f:
                content = f.read()
            content = content.replace("your_anthropic_api_key_here", api_key)
            with open(".env", "w") as f:
                f.write(content)
            print("✅ Anthropic API key configured")
    
    print("\n✅ Environment configuration complete!")
    return True


def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete!")
    
    print("Next steps:")
    print("1. Make sure FFmpeg is installed (required for audio)")
    print("2. Review your .env file and add any missing credentials")
    print("3. Invite your bot to your Discord server:")
    print("   - Go to Discord Developer Portal")
    print("   - Select your application")
    print("   - Go to OAuth2 > URL Generator")
    print("   - Select 'bot' scope and required permissions")
    print("   - Use the generated URL to invite the bot")
    print("4. Run the bot with: python bot.py")
    print("\nFor detailed instructions, see README.md")
    print("\n🎵 Happy music listening! 🎵\n")


def main():
    """Main setup function"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║            🎵 DiscordRecords Setup Wizard 🎵              ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check FFmpeg
    ffmpeg_ok = check_ffmpeg()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment file
    if not setup_env_file():
        sys.exit(1)
    
    # Print next steps
    print_next_steps()
    
    if not ffmpeg_ok:
        print("⚠️  WARNING: FFmpeg is not installed. The bot will not work without it!")


if __name__ == "__main__":
    main()
