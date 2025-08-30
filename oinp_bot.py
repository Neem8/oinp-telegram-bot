import requests
from bs4 import BeautifulSoup
import os
import time

# Telegram credentials from environment variables
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
URL = "https://www.ontario.ca/page/ontario-immigrant-nominee-program-oinp"
LAST_SEEN_FILE = "last_seen.txt"

def send_telegram(message):
    """Send a Telegram message"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send message: {e}")

def get_latest_update():
    """Scrape OINP page for latest update"""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        latest = soup.find("h3")  # Adjust selector if needed
        if latest:
            return latest.text.strip()
    except Exception as e:
        print(f"Error fetching OINP page: {e}")
    return None

def read_last_seen():
    """Read last seen update from file"""
    if os.path.exists(LAST_SEEN_FILE):
        with open(LAST_SEEN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def write_last_seen(update):
    """Write last seen update to file"""
    with open(LAST_SEEN_FILE, "w", encoding="utf-8") as f:
        f.write(update)

def main():
    last_seen = read_last_seen()
    latest = get_latest_update()
    
    # First run: send test alert
    if last_seen is None and latest:
        send_telegram(f"✅ OINP Bot is running! Latest update: {latest}")
        last_seen = latest
        write_last_seen(latest)

    while True:
        latest = get_latest_update()
        if latest and latest != last_seen:
            send_telegram(f"🚨 New OINP Update: {latest}")
            last_seen = latest
            write_last_seen(latest)
        time.sleep(20 * 60)  # 20 minutes

if __name__ == "__main__":
    main()
