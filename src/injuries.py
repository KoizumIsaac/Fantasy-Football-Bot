import json
from pathlib import Path

STATE_FILE = Path("injury_state.json")

def load_state(path=STATE_FILE):
    """Returns the saved {player_id: status} dict, or None on first run."""
    if not path.exists():
        return None
    return json.loads(path.read_text())

def save_state(state, path=STATE_FILE):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(path)  # swap in only after the write finished

def injury_changes(league, previous):
    """previous: {player_id: status} or None. Returns (changes, current)."""
    current, changes = {}, []
    for team in league.teams:
        for p in team.roster:
            pid = str(p.playerId)
            status = getattr(p, "injuryStatus", None) or "ACTIVE"
            current[pid] = status

            old = previous.get(pid) if previous else None
            if old is not None and old != status:
                changes.append({
                    "team": team.team_name,
                    "player": p.name,
                    "position": p.position,
                    "player_id": pid,
                    "old": old,
                    "new": status,
                })
    return changes, current