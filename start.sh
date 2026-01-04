#!/bin/bash
# Linux/macOS shell script to start the DiscordRecords bot

echo ""
echo "========================================"
echo "  Starting DiscordRecords Music Bot"
echo "========================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please run setup.py first or copy .env.example to .env"
    echo ""
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    echo ""
    exit 1
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "WARNING: FFmpeg not found"
    echo "The bot may not work without FFmpeg"
    echo ""
fi

# Start the bot
echo "Starting bot..."
echo ""
python3 bot.py

# If bot crashes, show message
if [ $? -ne 0 ]; then
    echo ""
    echo "Bot exited with an error"
    read -p "Press Enter to exit..."
fi
