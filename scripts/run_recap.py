import os
from dotenv import load_dotenv
from espn_api.football import League
from src.recap import build_recap
from src.discord import post_to_discord

load_dotenv()

league = League(
    league_id=int(os.environ["ESPN_LEAGUE_ID"]),
    year=int(os.environ["ESPN_YEAR"]),
    espn_s2=os.environ["ESPN_S2"],
    swid=os.environ["ESPN_SWID"],
)

week = league.current_week # last completed week

recap = build_recap(league.box_scores(week), week)
print(recap)
post_to_discord(recap)