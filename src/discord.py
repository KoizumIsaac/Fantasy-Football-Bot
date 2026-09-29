import os
import requests

def post_embed(embed):
    url = os.environ["DISCORD_WEBHOOK_URL"]
    resp = requests.post(url, json={"embeds": [embed]}, timeout=10)
    resp.raise_for_status()