BENCH_SLOTS = {"BE", "IR"}

def _starters(lineup):
    return [player for player in lineup if player.slot_position not in BENCH_SLOTS]

def _bench(lineup):
    return [player for player in lineup if player.slot_position == "BE"]

def _injured(lineup):
    return [player for player in lineup if player.slot_position == "IR"]

def top_scorer(box_scores):
    """Highest-scoring starter across the whole league this week."""
    best = None
    for match in box_scores:
        for team, lineup in ((match.home_team, match.home_lineup), (match.away_team, match.away_lineup)):
            for player in _starters(lineup):
                if best is None or player.points > best[0].points:
                    best = (player, team)
    return best

def blowout_and_closest(box_scores):
    """Returns (blowout, closest) as (margin, winner, loser) tuples."""
    results = []

    for match in box_scores:
        margin = abs(match.home_score - match.away_score)
        if match.home_score >= match.away_score:
            results.append((margin, match.home_team, match.away_team))
        else:
            results.append((margin, match.away_team, match.home_team))
    if not results:
        return None, None
    return max(results, key=lambda r : r[0]), min(results, key=lambda r : r[0])