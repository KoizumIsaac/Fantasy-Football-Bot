import os
from dotenv import load_dotenv
from espn_api.football import League
from src.recap import compute_recap
from src.formatting import build_embed
from src.discord import post_embeds

load_dotenv()

league = League(
    league_id=int(os.environ["ESPN_LEAGUE_ID"]),
    year=int(os.environ["ESPN_YEAR"]),
    espn_s2=os.environ["ESPN_S2"],
    swid=os.environ["ESPN_SWID"],
)

week = league.current_week - 1 # last completed week

recap = compute_recap(league.box_scores(week), week)
print(recap)  # handy for debugging
post_embeds([build_embed(recap)])