#!/usr/bin/env python3
"""
deploy.py - 24/7 Keep-Alive Bot (HEADLESS mode)
Uses portable Chromium + saved profile
Runs on Pterodactyl or any Linux server
"""

import os
import sys
import time
import logging
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
        print("Run manually: pip install -r requirements.txt")
        sys.exit(1)
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.os_manager import ChromeType
    from dotenv import load_dotenv

load_dotenv()

# Configuration
TARGET_URL = os.getenv("TARGET_URL", "https://idx.google.com")
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true").lower() == "true"
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "30"))

BASE_DIR = Path(__file__).parent
PROFILE_DIR = BASE_DIR / "portable_chrome_profile"
LOG_FILE = BASE_DIR / "keepalive.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def check_profile():
    """Verify profile folder exists"""
    if not PROFILE_DIR.exists() or not list(PROFILE_DIR.iterdir()):
        print()
        print("=" * 60)
        print(" ERROR: Profile Not Found!")
        print("=" * 60)
        print()
        print("You need to run setup.py first:")
        print("  1. python3 setup.py")
        print("  2. Log in to Google")
        print("  3. Close browser")
        print("  4. Then run this script")
        print()
        sys.exit(1)

def get_driver():
    """Create WebDriver with auto-downloaded ChromeDriver"""
    options = Options()
    options.add_argument(f"user-data-dir={PROFILE_DIR}")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    if HEADLESS_MODE:
        logging.info("Starting in HEADLESS mode")
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    else:
        logging.info("Starting in HEADFUL mode (visible window)")
    
    # Auto-download ChromeDriver
    service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(60)
    return driver

def keep_alive_loop():
    """Main keep-alive loop with auto-recovery"""
    driver = None
    consecutive_failures = 0
    
    while True:
        try:
            if driver is None:
                logging.info("=" * 60)
                logging.info("Starting browser...")
                logging.info(f"Target URL: {TARGET_URL}")
                logging.info("=" * 60)
                
                driver = get_driver()
                driver.get(TARGET_URL)
                
                title = driver.title
                logging.info(f"✓ Successfully opened: {title}")
                consecutive_failures = 0
            
            # Health check
            current_url = driver.current_url
            title = driver.title
            logging.info(f"[ALIVE] {title[:40]}... | {current_url[:50]}...")
            
            # Reset failure counter on success
            consecutive_failures = 0
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logging.info("Bot stopped by user")
            break
            
        except Exception as e:
            consecutive_failures += 1
            logging.error(f"[ERROR {consecutive_failures}] {type(e).__name__}: {e}")
            
            # Quit existing driver
            if driver:
                try:
                    driver.quit()
                except:
                    pass
                driver = None
            
            # Exponential backoff if many failures
            delay = min(10 * (2 ** min(consecutive_failures - 1, 4)), 300)
            logging.warning(f"Restarting in {delay} seconds...")
            time.sleep(delay)
    
    # Cleanup on exit
    if driver:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" GOOGLE IDX KEEP-ALIVE BOT (HEADLESS)")
    print("=" * 60)
    print(f" Target: {TARGET_URL}")
    print(f" Headless: {HEADLESS_MODE}")
    print(f" Check Interval: {CHECK_INTERVAL}s")
    print(f" Profile: {PROFILE_DIR}")
    print(f" Log File: {LOG_FILE}")
    print("=" * 60)
    print(" Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Verify profile exists
    check_profile()
    
    try:
        keep_alive_loop()
    except KeyboardInterrupt:
        logging.info("\n[STOPPED] Bot terminated by user")
        sys.exit(0)
