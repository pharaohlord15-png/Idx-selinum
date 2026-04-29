#!/usr/bin/env python3
"""
setup.py - Initial setup with HEADFUL browser (visible window)
Run this on your PC to log into Google IDX
Saves session to portable_chrome_profile/ folder
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# Auto-install dependencies
def install_requirements():
    """Install all required packages"""
    print("=" * 60)
    print(" Installing Dependencies...")
    print("=" * 60)
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("\n✓ All dependencies installed!\n")
        return True
    except subprocess.CalledProcessError:
        print("\n[ERROR] Failed to install dependencies")
        print("Try manually: pip install -r requirements.txt")
        return False

# Check and install if needed
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.os_manager import ChromeType
    from dotenv import load_dotenv
except ImportError:
    print("[INFO] Dependencies not found. Installing...")
    if not install_requirements():
        sys.exit(1)
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.os_manager import ChromeType
    from dotenv import load_dotenv

load_dotenv()

# Configuration
TARGET_URL = os.getenv("TARGET_URL", "")
BASE_DIR = Path(__file__).parent
PROFILE_DIR = BASE_DIR / "portable_chrome_profile"
ENV_FILE = BASE_DIR / ".env"

def log(msg):
    """Simple logger"""
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def get_target_url():
    """Get or prompt for target URL"""
    url = TARGET_URL
    
    if not url or url == "https://idx.google.com":
        print("\n" + "=" * 60)
        print(" Google IDX Keep-Alive Setup")
        print("=" * 60)
        url = input("\nEnter your Google IDX workspace URL: ").strip()
        
        if not url:
            print("[ERROR] URL is required!")
            sys.exit(1)
        
        if not url.startswith("http"):
            url = f"https://{url}"
        
        # Save to .env
        with open(ENV_FILE, "w") as f:
            f.write(f"TARGET_URL={url}\n")
            f.write("HEADLESS_MODE=false\n")
            f.write("CHECK_INTERVAL=30\n")
        
        log(f"✓ Saved configuration to .env")
    
    return url

def setup_browser():
    """Launch browser for login"""
    print("\n" + "=" * 60)
    print(" SETUP MODE - Login with VISIBLE Browser")
    print("=" * 60)
    print()
    print("This will:")
    print("  1. Download Chromium (if needed)")
    print("  2. Open a VISIBLE browser window")
    print("  3. Navigate to your Google IDX workspace")
    print("  4. You log in with your Google account")
    print("  5. Session is saved to portable_chrome_profile/")
    print()
    
    url = get_target_url()
    
    # Create profile directory
    PROFILE_DIR.mkdir(exist_ok=True)
    
    log(f"Target URL: {url}")
    log(f"Profile folder: {PROFILE_DIR}")
    log("Downloading ChromeDriver (one-time)...")
    
    options = Options()
    options.add_argument(f"user-data-dir={PROFILE_DIR}")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # HEADFUL mode - visible window
    # options.add_argument("--headless=new")  # Commented out = VISIBLE
    
    try:
        # Auto-download ChromeDriver
        service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        driver = webdriver.Chrome(service=service, options=options)
        
        log("")
        log(f"Opening: {url}")
        log("")
        log("=" * 60)
        log(" Browser is OPEN - Please LOG IN now")
        log(" CLOSE the browser window when finished")
        log("=" * 60)
        log("")
        
        driver.get(url)
        
        # Wait for user to close browser
        try:
            while True:
                try:
                    driver.current_url
                    time.sleep(1)
                except:
                    break
        except KeyboardInterrupt:
            log("Setup interrupted by user")
        
        driver.quit()
    
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        print("\nTroubleshooting:")
        print("  1. Install Chrome/Chromium: sudo apt install chromium-browser")
        print("  2. Or install Chrome: sudo apt install google-chrome-stable")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print(" ✓ Setup Complete!")
    print("=" * 60)
    print()
    print(f"Session saved to: {PROFILE_DIR}")
    print()
    print("Next steps:")
    print("  1. Test locally: python3 deploy.py")
    print("  2. Upload entire folder to Pterodactyl")
    print("  3. Run on server: python3 deploy.py")
    print()

if __name__ == "__main__":
    try:
        setup_browser()
    except KeyboardInterrupt:
        print("\n\n[STOPPED] Setup cancelled by user")
        sys.exit(0)
