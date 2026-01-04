@echo off
REM Windows batch script to start the DiscordRecords bot

echo.
echo ========================================
echo   Starting DiscordRecords Music Bot
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please run setup.py first or copy .env.example to .env
    echo.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    echo.
    pause
    exit /b 1
)

REM Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: FFmpeg not found in PATH
    echo The bot may not work without FFmpeg
    echo.
)

REM Start the bot
echo Starting bot...
echo.
python bot.py

REM If bot crashes, keep window open
if %errorlevel% neq 0 (
    echo.
    echo Bot exited with an error
    pause
)
