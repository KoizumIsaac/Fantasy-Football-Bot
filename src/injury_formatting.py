COLORS = {
    "OUT": 0xE74C3C,
    "INJURY_RESERVE": 0xE74C3C,
    "DOUBTFUL": 0xE67E22,
    "QUESTIONABLE": 0xF1C40F,
    "ACTIVE": 0x2ECC71,
}

LABELS = {
    "INJURY_RESERVE": "IR",
    "QUESTIONABLE": "Questionable",
    "DOUBTFUL": "Doubtful",
    "OUT": "Out",
    "ACTIVE": "Active",
}

def _label(status):
    return LABELS.get(status, status.replace("_", " ").title())

def build_injury_embed(change):
    embed = {
        "title": f"{change['player']} ({change['position']})",
        "description": (
            f"{_label(change['old'])} → **{_label(change['new'])}**\n"
            f"Rostered by {change['team']}"
        ),
        "color": COLORS.get(change["new"], 0x95A5A6),
    }
    # Optional headshot; Discord just shows nothing if the URL 404s
    embed["thumbnail"] = {
        "url": f"https://a.espncdn.com/i/headshots/nfl/players/full/{change['player_id']}.png"
    }
    return embed