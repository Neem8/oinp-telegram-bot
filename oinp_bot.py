import os
import requests
import schedule
import time
from datetime import datetime

# Telegram credentials from environment variables
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

def send_telegram(message):
    """Send a Telegram message"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload, timeout=10)
        print(f"Sent message: {message} at {datetime.now()}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def daily_message():
    send_telegram("🌞 Good morning!")

# Schedule the message every day at 4:00 AM
schedule.every().day.at("04:04").do(daily_message)

print("Telegram daily bot running...")

while True:
    schedule.run_pending()
    time.sleep(30)

