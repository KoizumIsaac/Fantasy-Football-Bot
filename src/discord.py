import os
import requests

def post_to_discord(text):
    url = os.environ["DISCORD_WEBHOOK_URL"]
    # Discord caps messages at 2000 characters
    resp = requests.post(url, json={"content": text[:2000]}, timeout=10)
    resp.raise_for_status()

def post_embed(title, description, fields, color=0x2ECC71):
    url = os.environ["DISCORD_WEBHOOK_URL"]
    payload = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": color,
            "fields": [
                {"name": n, "value": v, "inline": inline}
                for n, v, inline in fields
            ],
            "footer": {"text": "Fantasy Bot"},
        }]
    }
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()