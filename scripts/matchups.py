import os
from dotenv import load_dotenv
from espn_api.football import League

load_dotenv()

league = League(
    league_id=int(os.environ["ESPN_LEAGUE_ID"]),
    year=int(os.environ["ESPN_YEAR"]),
    espn_s2=os.environ["ESPN_S2"],
    swid=os.environ["ESPN_SWID"],
)

week = league.current_week
print(f"Week {week} matchups\n")

for m in league.box_scores(week):
    print(f"{m.home_team.team_name} {m.home_score} vs {m.away_score} {m.away_team.team_name}")