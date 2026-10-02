def _scoreboard_block(rows):
    lines = []
    for home, home_score, away, away_score in rows:
        lines.append(f"{home[:16]:<16} {home_score:>6.1f}")
        lines.append(f"{away[:16]:<16} {away_score:>6.1f}")
        lines.append("")
    return "```\n" + "\n".join(lines).rstrip() + "\n```"


def build_embed(recap):
    fields = []

    ts = recap["top_scorer"]
    if ts:
        fields.append({
            "name": "Top scorer",
            "value": f"{ts['player']} ({ts['points']:.1f}) for {ts['team']}",
            "inline": False,
        })

    b = recap["blowout"]
    if b:
        fields.append({
            "name": "Biggest blowout",
            "value": f"{b['winner']} beat {b['loser']} by {b['margin']:.1f}",
            "inline": True,
        })

    c = recap["closest"]
    if c:
        fields.append({
            "name": "Closest game",
            "value": f"{c['winner']} edged {c['loser']} by {c['margin']:.1f}",
            "inline": True,
        })

    w = recap["worst_bench"]
    if w:
        fields.append({
            "name": "Worst lineup call",
            "value": (
                f"{w['team']} benched {w['benched']} ({w['benched_points']:.1f}) "
                f"over {w['started']} ({w['started_points']:.1f})"
            ),
            "inline": False,
        })

    if recap["scoreboard"]:
        fields.append({
            "name": "Scoreboard",
            "value": _scoreboard_block(recap["scoreboard"])[:1024],
            "inline": False,
        })

    return {
        "title": f"Week {recap['week']} Recap",
        "color": 0x2ECC71,
        "fields": fields,
        "footer": {"text": "Fantasy Bot"},
    }