# 🚂 Railway Deployment Guide - Step by Step

## 📋 What You Need

- ✅ Railway account (free tier available)
- ✅ Your `portable_chrome_profile` folder from Windows
- ✅ GitHub account (for deployment)

---

## 🚀 Deployment Steps (Web Interface)

### Step 1: Prepare Your Repository

#### Option A: Use Existing GitHub Repo

1. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name: `idx-keepalive` (or any name)
   - Make it **Private** (your profile contains login session!)
   - Click "Create repository"

2. **Upload files to GitHub:**
   
   **Via Web Interface (Easiest):**
   - Go to your new repo
   - Click "uploading an existing file"
   - **Drag and drop ALL files:**
     ```
     ✓ deploy.py
     ✓ setup.py
     ✓ requirements.txt
     ✓ Procfile
     ✓ railway.json
     ✓ nixpacks.toml
     ✓ .env.example
     ✓ README.md
     ✓ portable_chrome_profile/ (ENTIRE FOLDER)
     ```
   - Click "Commit changes"

   **Via Git (Advanced):**
   ```bash
   cd idx-selenium
   git init
   git add .
   git commit -m "Initial deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/idx-keepalive.git
   git push -u origin main
   ```

#### Option B: Upload as ZIP (No GitHub)

If you don't want to use GitHub, you can deploy directly from Railway:
- Skip to Step 3 and use "Empty Project" method

---

### Step 2: Deploy to Railway from GitHub

1. **Go to Railway Dashboard:**
   - Visit: https://railway.app/new
   - Sign in with GitHub

2. **Create New Project:**
   - Click "Deploy from GitHub repo"
   - Click "Configure GitHub App"
   - Select your repository: `idx-keepalive`
   - Click "Deploy Now"

3. **Railway will auto-detect Python and start building**

---

### Step 3: Alternative - Deploy Without GitHub

1. **Go to Railway Dashboard:**
   - Visit: https://railway.app/new
   - Click "Empty Project"

2. **Upload via Railway CLI:**
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login
   railway login
   
   # Link to your project
   railway link
   
   # Deploy
   railway up
   ```

---

### Step 4: Configure Environment Variables

1. **In Railway Dashboard:**
   - Click on your deployed service
   - Go to **"Variables"** tab
   - Click **"+ New Variable"**

2. **Add these variables:**
   ```
   TARGET_URL = https://idx.google.com/u/2/pharaoh-34024394
   HEADLESS_MODE = true
   CHECK_INTERVAL = 30
   ```

3. **Click "Save"**

---

### Step 5: Install Chromium (Critical!)

Railway needs Chromium installed. We use `nixpacks.toml` for this.

**Verify nixpacks.toml is in your repo:**
```toml
[phases.setup]
nixPkgs = ["python39", "chromium"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "python3 deploy.py"
```

If not detected automatically:

1. **In Railway Dashboard:**
   - Go to "Settings" tab
   - Scroll to "Deploy"
   - Under "Custom Start Command" add:
     ```
     python3 deploy.py
     ```

2. **Trigger Redeploy:**
   - Go to "Deployments" tab
   - Click "⋮" menu on latest deployment
   - Click "Redeploy"

---

### Step 6: Verify Deployment

1. **Check Logs:**
   - In Railway Dashboard
   - Click on your service
   - Go to "Deployments" tab
   - Click on the active deployment
   - View logs in real-time

2. **You should see:**
   ```
   ============================================================
    GOOGLE IDX KEEP-ALIVE BOT (HEADLESS)
   ============================================================
    Target: https://idx.google.com/u/2/pharaoh-34024394
    Headless: True
   ============================================================
   
   2026-04-28 14:06:05 - INFO - Starting in HEADLESS mode
   2026-04-28 14:06:10 - INFO - ✓ Successfully opened: Google IDX
   2026-04-28 14:06:40 - INFO - [ALIVE] Google IDX...
   ```

3. **If you see errors:** Check troubleshooting section below

---

## 📁 Required File Structure on Railway

```
your-repo/
├── deploy.py                    # Main bot script
├── setup.py                     # (Optional - not used on Railway)
├── requirements.txt             # Python dependencies
├── Procfile                     # Railway start command
├── railway.json                 # Railway config
├── nixpacks.toml               # Chromium installation
├── .env.example                 # Example config
├── portable_chrome_profile/     # 🔥 YOUR PROFILE FROM WINDOWS
│   ├── Default/
│   ├── IndexedDB/
│   └── ...
└── README.md
```

**⚠️ CRITICAL: Include your `portable_chrome_profile` folder!**

---

## 🔧 Railway Configuration Files

### Procfile
```
web: python3 deploy.py
```

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "python3 deploy.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### nixpacks.toml
```toml
[phases.setup]
nixPkgs = ["python39", "chromium"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "python3 deploy.py"
```

---

## 🐛 Troubleshooting

### Error: "Profile not found"

**Cause:** `portable_chrome_profile` folder missing

**Solution:**
```bash
# Make sure your GitHub repo has the profile folder
# Check on GitHub - you should see:
# your-repo/portable_chrome_profile/Default/

# If missing, add it:
git add portable_chrome_profile/
git commit -m "Add Chrome profile"
git push
```

### Error: "Chrome binary not found"

**Cause:** Chromium not installed

**Solution:**
1. Verify `nixpacks.toml` exists in your repo
2. Make sure it contains: `nixPkgs = ["python39", "chromium"]`
3. Redeploy in Railway dashboard

### Error: "Session not created"

**Cause:** ChromeDriver version mismatch

**Solution:**
The script auto-downloads ChromeDriver using `webdriver-manager`. Check logs:
```
# Should see:
WebDriver manager - Get LATEST chromedriver version
```

If not, add to your `deploy.py`:
```python
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
```

### Build Fails

**Check Railway logs:**
1. Go to "Deployments" tab
2. Click failed deployment
3. View build logs

**Common fixes:**
```bash
# Update requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## 💰 Railway Pricing (As of 2024)

- **Free Tier:** $5 credit/month
- **Execution hours:** ~500 hours/month free
- **After free tier:** Pay as you go

**This bot uses minimal resources:**
- ~150-300 MB RAM
- Runs 24/7 = 730 hours/month
- Fits in free tier if you have no other services

---

## 🔄 Updating Your Deployment

### Update Code:
```bash
# Make changes locally
git add .
git commit -m "Update bot"
git push

# Railway auto-deploys on push
```

### Update Environment Variables:
1. Railway Dashboard
2. Click your service
3. Go to "Variables" tab
4. Edit variables
5. Click "Save" (auto-redeploys)

### Manual Redeploy:
1. Go to "Deployments" tab
2. Click "⋮" on latest deployment
3. Click "Redeploy"

---

## 🔒 Security Notes

**⚠️ IMPORTANT: Your profile contains login cookies!**

1. **Make GitHub repo PRIVATE**
   - Go to repo Settings
   - Scroll to "Danger Zone"
   - Change visibility to Private

2. **Don't commit .env file**
   - Use Railway environment variables instead
   - `.env` should be in `.gitignore`

3. **Rotate session periodically**
   - Log out and log back in every few months
   - Run `setup.py` locally to refresh profile

---

## 📊 Monitoring

### View Logs in Real-Time:
1. Railway Dashboard
2. Click your service
3. Go to "Deployments" tab
4. Click active deployment
5. Logs stream live

### Download Logs:
Railway doesn't provide log download, but you can:
- Copy from web interface
- Use Railway CLI: `railway logs`

---

## ✅ Quick Checklist

Before deploying to Railway:

- [ ] `portable_chrome_profile/` folder added to repo
- [ ] `Procfile` created
- [ ] `railway.json` created  
- [ ] `nixpacks.toml` created
- [ ] Environment variables set in Railway
- [ ] GitHub repo is PRIVATE
- [ ] Profile folder has `Default/`, `IndexedDB/` etc.

---

## 🎯 Expected Result

After successful deployment:

```
Build: ✅ Success
Deploy: ✅ Active
Logs: ✅ "[ALIVE] Google IDX..."

Your bot is now running 24/7 on Railway!
```

---

## 🆘 Still Having Issues?

1. **Check Railway Status:** https://railway.statuspage.io/
2. **Railway Discord:** https://discord.gg/railway
3. **View full logs** in Railway dashboard
4. **Test locally first:**
   ```bash
   python3 deploy.py
   ```
   If it works locally but not on Railway, it's a Railway config issue.

---

**Need help? Check the logs first - they tell you everything!** 📝
