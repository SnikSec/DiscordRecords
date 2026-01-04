# 🚀 Deployment Guide

How to deploy DiscordRecords for 24/7 operation.

## Deployment Options

### Option 1: Home Computer/Server (Free)
**Pros**: Free, full control, no limitations
**Cons**: Requires computer to stay on 24/7, uses your internet

**Setup**:
1. Follow normal installation steps
2. Run `python bot.py` or use `start.bat`/`start.sh`
3. Keep terminal window open
4. For Windows: Create a scheduled task to auto-start on boot
5. For Linux: Create a systemd service (see below)

### Option 2: VPS (Virtual Private Server) (~$5-10/month)
**Providers**: DigitalOcean, Linode, Vultr, OVH
**Pros**: Reliable, fast, dedicated resources
**Cons**: Costs money, requires basic Linux knowledge

**Recommended Setup**:
```bash
# 1. Create VPS with Ubuntu 22.04
# 2. SSH into your server
ssh user@your-server-ip

# 3. Install Python and FFmpeg
sudo apt update
sudo apt install python3 python3-pip ffmpeg git -y

# 4. Clone your repo
git clone https://github.com/yourusername/DiscordRecords.git
cd DiscordRecords

# 5. Install dependencies
pip3 install -r requirements.txt

# 6. Create .env file
nano .env
# Add your credentials, save (Ctrl+X, Y, Enter)

# 7. Test the bot
python3 bot.py

# 8. Set up as systemd service (see below)
```

### Option 3: Cloud Platforms

#### Heroku (Free tier ended, now paid)
Not recommended due to removed free tier.

#### Railway.app (Free $5/month credit)
**Pros**: Easy deployment, free credits
**Cons**: Limited free tier

**Setup**:
1. Create account at [Railway.app](https://railway.app)
2. Connect GitHub repository
3. Add environment variables in dashboard:
   - `DISCORD_TOKEN`
   - `SPOTIFY_CLIENT_ID` (optional)
   - `SPOTIFY_CLIENT_SECRET` (optional)
   - `ANTHROPIC_API_KEY` (optional)
4. Deploy automatically

#### Replit (Free tier available)
**Pros**: Very easy, no setup needed
**Cons**: Limited resources, may sleep

**Setup**:
1. Import from GitHub to [Replit](https://replit.com)
2. Add secrets in the Secrets tab (lock icon)
3. Click Run
4. Use UptimeRobot to keep it awake

### Option 4: Oracle Cloud (Free Forever Tier)
**Pros**: Actually free forever, generous resources
**Cons**: Requires more setup

Oracle offers always-free VMs that are perfect for Discord bots.

## Keeping Bot Running 24/7

### Linux Systemd Service (Recommended for VPS)

Create `/etc/systemd/system/discordrecords.service`:

```ini
[Unit]
Description=DiscordRecords Music Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser/DiscordRecords
ExecStart=/usr/bin/python3 /home/youruser/DiscordRecords/bot.py
Restart=always
RestartSec=10
StandardOutput=append:/home/youruser/DiscordRecords/bot.log
StandardError=append:/home/youruser/DiscordRecords/bot.error.log

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable discordrecords
sudo systemctl start discordrecords

# Check status
sudo systemctl status discordrecords

# View logs
journalctl -u discordrecords -f
```

### Windows Auto-Start

**Method 1: Task Scheduler**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: "When the computer starts"
4. Action: "Start a program"
5. Program: `C:\Path\To\Python\python.exe`
6. Arguments: `C:\Path\To\DiscordRecords\bot.py`
7. Start in: `C:\Path\To\DiscordRecords`

**Method 2: Startup Folder**
1. Press `Win+R`, type `shell:startup`
2. Create shortcut to `start.bat`
3. Place in startup folder

### Screen/Tmux (Simple VPS Solution)

Using `screen`:
```bash
# Start a screen session
screen -S discordbot

# Run the bot
python3 bot.py

# Detach (keep running): Ctrl+A then D

# Reattach later
screen -r discordbot
```

Using `tmux`:
```bash
# Start tmux
tmux new -s discordbot

# Run the bot
python3 bot.py

# Detach: Ctrl+B then D

# Reattach later
tmux attach -t discordbot
```

## Environment Variables for Production

### Method 1: .env file (Local/VPS)
```bash
DISCORD_TOKEN=your_token_here
BOT_PREFIX=!
SPOTIFY_CLIENT_ID=your_id
SPOTIFY_CLIENT_SECRET=your_secret
ANTHROPIC_API_KEY=your_key
```

### Method 2: Export (VPS)
Add to `~/.bashrc`:
```bash
export DISCORD_TOKEN="your_token_here"
export BOT_PREFIX="!"
```

### Method 3: Systemd Environment (VPS)
In your service file:
```ini
[Service]
Environment="DISCORD_TOKEN=your_token"
Environment="BOT_PREFIX=!"
```

### Method 4: Docker (Advanced)
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  bot:
    build: .
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - BOT_PREFIX=${BOT_PREFIX}
      - SPOTIFY_CLIENT_ID=${SPOTIFY_CLIENT_ID}
      - SPOTIFY_CLIENT_SECRET=${SPOTIFY_CLIENT_SECRET}
    restart: unless-stopped
```

## Monitoring & Maintenance

### Check if Bot is Running

**Linux**:
```bash
# If using systemd
systemctl status discordrecords

# Check process
ps aux | grep bot.py

# Check logs
tail -f bot.log
```

**Windows**:
```powershell
# Check running Python processes
Get-Process python
```

### Automatic Restarts

The bot includes error handling, but for crashes:

**Linux systemd**: Already configured with `Restart=always`

**PM2** (Cross-platform process manager):
```bash
npm install -g pm2
pm2 start bot.py --name discordrecords --interpreter python3
pm2 startup  # Enable on boot
pm2 save
```

### Log Rotation

For Linux (`/etc/logrotate.d/discordrecords`):
```
/home/youruser/DiscordRecords/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

## Performance Optimization

### For Low-Resource Servers

1. **Reduce audio quality** in `music/player.py`:
```python
self.ytdl_options = {
    'format': 'worstaudio/worst',  # Lower quality
    # ...
}
```

2. **Limit queue size**:
```python
MAX_QUEUE_SIZE = 20  # Add to player.py
```

3. **Disable AI** (just don't set `ANTHROPIC_API_KEY`)

4. **Use swap space** on Linux:
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Cost Estimates

### Monthly Costs

| Component | Cost | Required? |
|-----------|------|-----------|
| Discord Bot Token | FREE | ✅ Yes |
| FFmpeg | FREE | ✅ Yes |
| Spotify API | FREE | ❌ Optional |
| YouTube (via yt-dlp) | FREE | ✅ Yes |
| Anthropic API | $3-15 | ❌ Optional |
| VPS Hosting | $0-10 | ❌ Optional |
| **Total (Minimal)** | **$0** | - |
| **Total (Full Features + VPS)** | **$5-25** | - |

### Free 24/7 Options

1. **Home computer** - $0 (electricity only)
2. **Oracle Cloud Free Tier** - $0
3. **Railway.app** - $5 free credits/month
4. **Replit** - Free with limitations

## Updating Deployed Bot

### VPS/Linux
```bash
cd DiscordRecords
git pull origin main
pip3 install -r requirements.txt --upgrade
sudo systemctl restart discordrecords
```

### Docker
```bash
docker-compose pull
docker-compose up -d --build
```

### Cloud Platforms
Most auto-deploy on git push.

## Troubleshooting Deployment

### Bot Goes Offline Randomly

**Cause**: Process crashed or server restarted
**Solution**: 
- Use systemd or PM2 with auto-restart
- Check logs for errors
- Ensure adequate RAM (512MB minimum)

### High CPU Usage

**Cause**: FFmpeg encoding or too many songs queued
**Solution**:
- Reduce audio quality
- Limit queue size
- Use a more powerful server

### Connection Timeouts

**Cause**: Network issues or Discord API problems
**Solution**:
- Check server internet connection
- Verify firewall rules
- Bot auto-reconnects on connection loss

## Security Best Practices

1. **Never commit** `.env` files
2. **Use SSH keys** for VPS access, not passwords
3. **Keep system updated**: `sudo apt update && sudo apt upgrade`
4. **Run bot as non-root user**
5. **Use firewall**: `sudo ufw enable`
6. **Regular backups** of configuration

## Recommended VPS Specs

**Minimum**:
- 512 MB RAM
- 1 CPU core
- 10 GB storage
- Any Linux distro (Ubuntu recommended)

**Recommended**:
- 1 GB RAM
- 2 CPU cores  
- 20 GB storage
- Ubuntu 22.04 LTS

## Need Help?

- Check bot logs first
- Test locally before deploying
- Use Discord webhooks for error notifications
- Join Discord communities for hosting questions

---

**Pro Tip**: Start with running on your home computer, then upgrade to VPS when you need 24/7 reliability!
