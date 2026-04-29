# 🚀 Google IDX Keep-Alive Bot (Linux/Pterodactyl)

Simple Selenium-based browser automation that keeps your Google IDX workspace alive 24/7.

## 📦 Features

- ✅ **Auto-installs everything** - Dependencies, ChromeDriver, all automatic
- ✅ **Separate scripts** - `setup.py` (headful) and `deploy.py` (headless)
- ✅ **Portable profile** - Login once, run anywhere
- ✅ **Linux-native** - Built for Ubuntu/Debian/Pterodactyl
- ✅ **Lightweight** - < 10KB upload, ~150MB after install
- ✅ **Auto-recovery** - Restarts on crashes with exponential backoff

---

## 🚀 Quick Start

### Step 1: Setup on Your PC/VPS (One-Time Login)

```bash
# Clone or upload this folder
cd idx-selenium

# Run setup - opens VISIBLE browser
python3 setup.py
```

**What happens:**
1. Auto-installs: `selenium`, `webdriver-manager`, `python-dotenv`
2. Downloads ChromeDriver automatically
3. Opens a **VISIBLE** browser window
4. You log into Google IDX
5. You close the browser
6. Session saved to `portable_chrome_profile/`

### Step 2: Deploy (24/7 Headless Mode)

```bash
# Run the bot
python3 deploy.py
```

**What happens:**
1. Auto-installs dependencies (if needed)
2. Checks for profile folder
3. Starts in **HEADLESS** mode (invisible)
4. Keeps workspace alive 24/7
5. Auto-recovers from crashes

---

## 📋 Files Explained

| File | Purpose | Mode |
|------|---------|------|
| `setup.py` | Initial login | **Headful** (visible) |
| `deploy.py` | 24/7 keep-alive | **Headless** (invisible) |
| `requirements.txt` | Dependencies | Auto-installed |
| `portable_chrome_profile/` | Your session | Created by setup.py |
| `.env` | Configuration | Auto-created |

---

## ⚙️ Configuration

Edit `.env` or set environment variables:

```env
TARGET_URL=https://idx.google.com/u/2/your-workspace-id
HEADLESS_MODE=true
CHECK_INTERVAL=30
```

---

## 🎮 Pterodactyl Deployment

### Method 1: Pre-Login on Local Machine (Recommended)

```bash
# On your PC/VPS with desktop:
python3 setup.py
# Log in when browser opens
# Close browser when done

# Upload entire folder to Pterodactyl
# (includes portable_chrome_profile/)

# Startup command on Pterodactyl:
python3 deploy.py
```

### Method 2: Direct on Server (if you have VNC access)

```bash
# Upload folder to Pterodactyl
# Connect via VNC
# Run: python3 setup.py
# Then: python3 deploy.py
```

---

## 🔧 System Requirements

### On Setup Machine (where you log in):
- Python 3.7+
- Display server (X11, Wayland, or VNC)
- Chrome/Chromium installed

### On Deploy Machine (Pterodactyl):
- Python 3.7+
- Chrome/Chromium installed
- No display needed (headless)

### Installing Chrome on Linux:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install chromium-browser

# Or Google Chrome stable
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt install -f
```

---

## 📁 Folder Structure

```
idx-selenium/
├── setup.py                      # Setup script (headful)
├── deploy.py                     # Deploy script (headless)
├── requirements.txt              
├── .env.example                 
├── .env                          # Created after setup
├── portable_chrome_profile/      # Your Google session ⭐
│   ├── Default/
│   ├── IndexedDB/
│   └── ...
├── keepalive.log                 # Bot activity log
└── README.md
```

**The `portable_chrome_profile/` folder is your login session - keep it safe!**

---

## 💡 How It Works

### Setup Phase (setup.py)
1. Installs dependencies via pip
2. Downloads ChromeDriver using webdriver-manager
3. Launches Chrome in **HEADFUL** mode (visible window)
4. You log into Google
5. Saves cookies/session to `portable_chrome_profile/`

### Deploy Phase (deploy.py)
1. Checks for `portable_chrome_profile/`
2. Launches Chrome in **HEADLESS** mode (invisible)
3. Loads your saved session
4. Keeps IDX workspace tab open 24/7
5. Monitors health every 30 seconds
6. Auto-restarts on crashes

---

## 📊 Resource Usage

- **RAM:** ~150-300 MB (headless Chromium)
- **CPU:** < 5% idle, < 20% on page loads
- **Disk:** 
  - Upload: ~8 KB
  - ChromeDriver: ~10 MB
  - Chromium (system): ~100-150 MB
  - Profile: ~10-20 MB
  - Total: ~150 MB

---

## 🐛 Troubleshooting

### "Profile not found" error
**Solution:** Run `python3 setup.py` first to create the profile.

### "Chrome binary not found"
**Solution:** Install Chrome/Chromium:
```bash
sudo apt install chromium-browser
# OR
sudo apt install google-chrome-stable
```

### "Dependencies not found"
**Solution:** Both scripts auto-install. If manual install needed:
```bash
pip3 install -r requirements.txt
```

### Session keeps logging out
**Solution:**
1. Make sure you uploaded `portable_chrome_profile/` folder
2. Check folder permissions (must be readable by bot user)
3. Google may require 2FA - consider using App Passwords

### "webdriver-manager" errors
**Solution:** Clear cache and reinstall:
```bash
rm -rf ~/.wdm
pip3 install --upgrade webdriver-manager
```

---

## 📝 Logs

All activity is logged to `keepalive.log`:

```bash
# View live logs
tail -f keepalive.log

# View last 50 lines
tail -50 keepalive.log

# Search for errors
grep ERROR keepalive.log
```

---

## 🔒 Security Notes

- `portable_chrome_profile/` contains your Google cookies
- Keep this folder **private**
- Don't commit to git (see `.gitignore`)
- Use a dedicated Google account for automation
- Consider using Google App Passwords instead of main password

---

## 🎯 Perfect For

- ✅ Google IDX workspace keep-alive
- ✅ Pterodactyl hosting panels
- ✅ Ubuntu/Debian VPS servers
- ✅ Raspberry Pi (ARM compatible)
- ✅ Docker containers
- ✅ Any Linux environment

---

## 🔄 Updating

To update dependencies:

```bash
pip3 install --upgrade -r requirements.txt
```

---

## ❓ FAQ

**Q: Can I run this on Windows?**  
A: This version is optimized for Linux. For Windows, the Chromium paths would need to change from `chrome` to `chrome.exe`.

**Q: Do I need to keep running setup.py?**  
A: No! Run it once to log in, then only use `deploy.py`.

**Q: Can I use this for other websites?**  
A: Yes! Just change `TARGET_URL` in `.env`.

**Q: How do I stop the bot?**  
A: Press `Ctrl+C` in the terminal.

**Q: Will my session expire?**  
A: Google sessions can last weeks/months. The bot keeps the workspace active to prevent timeout.

**Q: Can I run multiple instances?**  
A: Yes, but use separate folders with different profiles.

---

## 📚 Learn More

- **Selenium Docs:** https://selenium-python.readthedocs.io/
- **WebDriver Manager:** https://github.com/SergeyPirogov/webdriver_manager
- **Chrome Flags:** https://peter.sh/experiments/chromium-command-line-switches/

---

## ⚖️ License

MIT - Free to use and modify

---

**Built for automation enthusiasts who need reliable, simple solutions** 🚀
