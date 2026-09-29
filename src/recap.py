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

def build_recap(box_scores, week):
    lines = [f"Week {week} recap", ""]

    top_score = top_scorer(box_scores)
    if top_score:
        player, team = top_score
        lines.append(f"Top scorer: {player.name} ({player.points:.1f}) for {team.team_name}")

    blowout, closest = blowout_and_closest(box_scores)
    if blowout:
        lines.append(f"Biggest blowout: {blowout[1].team_name} beat {blowout[2].team_name} by {blowout[0]:.1f}")
        lines.append(f"Closest game: {closest[1].team_name} edged {closest[2].team_name} by {closest[0]:.1f}")

    missed = bench_points_missed(box_scores)
    if missed:
        gap, team, bencher, starter = missed[0]
        lines.append(
            f"Worst lineup call: {team.team_name} benched {bencher.name} "
            f"({bencher.points:.1f}) over {starter.name} ({starter.points:.1f})"
        )

    return "\n".join(lines)