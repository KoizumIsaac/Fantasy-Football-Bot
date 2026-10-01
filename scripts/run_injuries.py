import os
from dotenv import load_dotenv
from espn_api.football import League

from src.injuries import load_state, save_state, injury_changes
from src.injury_formatting import build_injury_embed
from src.discord import post_embeds

load_dotenv()

league = League(
    league_id=int(os.environ["ESPN_LEAGUE_ID"]),
    year=int(os.environ["ESPN_YEAR"]),
    espn_s2=os.environ["ESPN_S2"],
    swid=os.environ["ESPN_SWID"],
)

previous = load_state()
changes, current = injury_changes(league, previous)

if previous is None:
    print(f"First run: saved baseline for {len(current)} players, nothing posted.")
elif changes:
    post_embeds(
        [build_injury_embed(c) for c in changes],
        webhook_env="DISCORD_INJURY_WEBHOOK_URL",
    )
    print(f"Posted {len(changes)} injury update(s).")
else:
    print("No changes.")

# Save only after posting succeeds, so a failed post gets retried next run
save_state(current)