import os
import requests

def post_to_discord(text):
    url = os.environ["DISCORD_WEBHOOK_URL"]
    # Discord caps messages at 2000 characters
    resp = requests.post(url, json={"content": text[:2000]}, timeout=10)
    resp.raise_for_status()