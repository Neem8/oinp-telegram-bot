import requests
from bs4 import BeautifulSoup
import os
import time

# Telegram credentials from environment variables
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
URL = "https://www.ontario.ca/page/ontario-immigrant-nominee-program-oinp"

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
        # Adjust selector to match the latest round header
        latest = soup.find("h3")
        if latest:
            return latest.text.strip()
    except Exception as e:
        print(f"Error fetching OINP page: {e}")
    return None

def main():
    last_seen = None
    while True:
        latest = get_latest_update()
        if latest and latest != last_seen:
            send_telegram(f"🚨 New OINP Update: {latest}")
            last_seen = latest
        # Sleep 20 minutes
        time.sleep(20 * 60)

if __name__ == "__main__":
    main()
