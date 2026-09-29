BENCH_SLOTS = {"BE", "IR"}

def _starters(lineup):
    return [player for player in lineup if player.slot_position not in BENCH_SLOTS]

def _bench(lineup):
    return [player for player in lineup if player.slot_position == "BE"]

def _injured(lineup):
    return [player for player in lineup if player.slot_position == "IR"]

def _margin(result):
    if result is None:
        return None
    margin, winner, loser = result
    return {"margin": margin, "winner": winner.team_name, "loser": loser.team_name}

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

def bench_points_missed(box_scores):
    """
    For each team, find bench players who outscored the lowest-scoring
    starter at their same position. Simplified: ignores flex-slot eligibility.
    """
    missed = []
    for m in box_scores:
        for team, lineup in ((m.home_team, m.home_lineup), (m.away_team, m.away_lineup)):
            starters = _starters(lineup)
            for benched in _bench(lineup):
                same_position = [starter for starter in starters if starter.position == benched.position]
                if not same_position:
                    continue
                worst = min(same_position, key=lambda s: s.points)
                if benched.points > worst.points:
                    missed.append((benched.points - worst.points, team, benched, worst))
    return sorted(missed, key=lambda r: r[0], reverse=True)

def compute_recap(box_scores, week):
    ts = top_scorer(box_scores)
    blowout, closest = blowout_and_closest(box_scores)
    missed = bench_points_missed(box_scores)

    worst_bench = None
    if missed:
        gap, team, bench_p, starter_p = missed[0]
        worst_bench = {
            "team": team.team_name,
            "benched": bench_p.name,
            "benched_points": bench_p.points,
            "started": starter_p.name,
            "started_points": starter_p.points,
        }

    return {
        "week": week,
        "top_scorer": (
            {"player": ts[0].name, "points": ts[0].points, "team": ts[1].team_name}
            if ts else None
        ),
        "blowout": _margin(blowout),
        "closest": _margin(closest),
        "worst_bench": worst_bench,
        "scoreboard": [
            (m.home_team.team_name, m.home_score, m.away_team.team_name, m.away_score)
            for m in box_scores
        ],
    }