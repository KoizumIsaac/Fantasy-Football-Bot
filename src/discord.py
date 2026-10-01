import os
import requests

def post_embeds(embeds, webhook_env="DISCORD_WEBHOOK_URL"):
    url = os.environ[webhook_env]
    # Discord allows at most 10 embeds per message
    for i in range(0, len(embeds), 10):
        resp = requests.post(url, json={"embeds": embeds[i:i + 10]}, timeout=10)
        resp.raise_for_status()