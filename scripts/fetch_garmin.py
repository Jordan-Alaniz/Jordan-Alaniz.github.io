#!/usr/bin/env python3
"""
fetch_garmin.py — pulls recent running activities from Garmin Connect
and writes _data/training_log.json for the Jekyll site.

Setup:
  1. Store GARMIN_EMAIL and GARMIN_PASSWORD as GitHub repository secrets.
  2. Optional: store GARMIN_TOKENSTORE (base64-encoded garth token dir) for
     MFA-protected accounts (see README for one-time token export steps).

Usage (CI):
  pip install garminconnect
  python scripts/fetch_garmin.py
"""

import json
import math
import os
import sys
import base64
import tempfile
from datetime import datetime, timezone

# ── Install check ──────────────────────────────────────────────────────────────
try:
    import garminconnect
except ImportError:
    print("ERROR: garminconnect not installed. Run: pip install garminconnect")
    sys.exit(1)

# ── Constants ─────────────────────────────────────────────────────────────────
REPO_ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH  = os.path.join(REPO_ROOT, "_data", "training_log.json")
ACTIVITY_LIMIT = 30   # how many recent activities to fetch
RUN_TYPES    = {"running", "track_running", "treadmill_running", "indoor_running",
                "trail_running", "virtual_run"}

# Workout-type mapping from Garmin activityType → display label
WORKOUT_LABELS = {
    "easy":        "Easy Run",
    "long_run":    "Long Run",
    "tempo":       "Tempo",
    "interval":    "Intervals",
    "race":        "Race",
    "recovery":    "Recovery",
    "warmup":      "Warm-up",
    "cooldown":    "Cool-down",
}

# ── Helper: seconds → "M:SS" ──────────────────────────────────────────────────
def fmt_pace(secs_per_mile: float) -> str:
    if secs_per_mile <= 0 or math.isinf(secs_per_mile):
        return "—"
    m = int(secs_per_mile // 60)
    s = int(secs_per_mile % 60)
    return f"{m}:{s:02d}"

def fmt_duration(total_seconds: float) -> str:
    total_seconds = int(total_seconds)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

def meters_to_miles(m: float) -> float:
    return round(m / 1609.344, 2)

# ── Garmin auth ───────────────────────────────────────────────────────────────
def get_client() -> garminconnect.Garmin:
    token_b64 = os.environ.get("GARMIN_TOKENSTORE")
    email     = os.environ.get("GARMIN_EMAIL", "")
    password  = os.environ.get("GARMIN_PASSWORD", "")

    if token_b64:
        token_dir = tempfile.mkdtemp(prefix="garth_")
        token_bytes = base64.b64decode(token_b64)
        oauth_path = os.path.join(token_dir, "oauth2_token.json")
        with open(oauth_path, "wb") as f:
            f.write(token_bytes)
        client = garminconnect.Garmin()
        client.garth.load(token_dir)
        return client

    if not email or not password:
        print("ERROR: Set GARMIN_EMAIL + GARMIN_PASSWORD (or GARMIN_TOKENSTORE) as secrets.")
        sys.exit(1)

    client = garminconnect.Garmin(email, password)
    client.login()
    return client

# ── Activity → dict ───────────────────────────────────────────────────────────
def parse_activity(raw: dict, client) -> dict | None:
    atype = raw.get("activityType", {}).get("typeKey", "")
    if atype not in RUN_TYPES:
        return None

    act_id      = str(raw.get("activityId", ""))
    distance_m  = float(raw.get("distance", 0) or 0)
    duration_s  = float(raw.get("duration", 0) or 0)
    distance_mi = meters_to_miles(distance_m)

    # Speed in m/s → pace in sec/mile
    speed_ms    = float(raw.get("averageSpeed", 0) or 0)
    pace_secmi  = (1609.344 / speed_ms) if speed_ms > 0 else 0

    # Date/day
    start_raw   = raw.get("startTimeLocal", raw.get("startTimeGMT", ""))
    try:
        dt = datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
    except Exception:
        dt = datetime.now(timezone.utc)
    date_str = dt.strftime("%Y-%m-%d")
    day_str  = dt.strftime("%a")

    # Workout type label
    workout_key   = (raw.get("workoutType") or "").lower()
    activity_name = (raw.get("activityName") or "").lower()
    if "interval" in activity_name or "track" in atype:
        w_label = "Intervals"
        w_type  = "interval"
    elif "tempo" in activity_name or "threshold" in activity_name:
        w_label = "Tempo"
        w_type  = "tempo"
    elif "long" in activity_name:
        w_label = "Long Run"
        w_type  = "long"
    elif "recovery" in activity_name or "recover" in activity_name:
        w_label = "Recovery"
        w_type  = "easy"
    elif "race" in activity_name or "meet" in activity_name:
        w_label = "Race"
        w_type  = "race"
    else:
        w_label = WORKOUT_LABELS.get(workout_key, "Easy Run")
        w_type  = "easy"

    # HR
    avg_hr = int(raw.get("averageHR") or 0)
    max_hr = int(raw.get("maxHR") or 0)

    # Laps
    laps = []
    try:
        splits = client.get_activity_splits(int(act_id))
        lap_dtos = splits.get("lapDTOs", [])
        for i, lap in enumerate(lap_dtos, 1):
            lap_dist_m  = float(lap.get("distance", 0) or 0)
            lap_dur_s   = float(lap.get("duration", 0) or 0)
            lap_speed   = float(lap.get("averageSpeed", 0) or 0)
            lap_pace_s  = (1609.344 / lap_speed) if lap_speed > 0 else 0
            lap_hr      = int(lap.get("averageHR") or 0)
            laps.append({
                "n":    i,
                "dist": str(round(meters_to_miles(lap_dist_m), 2)),
                "time": fmt_duration(lap_dur_s),
                "pace": fmt_pace(lap_pace_s),
                "hr":   lap_hr,
            })
    except Exception:
        pass  # laps are optional

    return {
        "id":           act_id,
        "date":         date_str,
        "day":          day_str,
        "type":         w_type,
        "type_label":   w_label,
        "distance_mi":  distance_mi,
        "duration":     fmt_duration(duration_s),
        "pace":         fmt_pace(pace_secmi),
        "avg_hr":       avg_hr,
        "max_hr":       max_hr,
        "notes":        (raw.get("description") or "").strip(),
        "laps":         laps,
    }

# ── Season start: first Monday on or before Feb 1 of current year ────────────
def season_start() -> "date":
    from datetime import date
    today = date.today()
    # Outdoor season starts ~Feb 1; XC ~Aug 1. Pick whichever is most recent.
    year = today.year
    candidates = [date(year, 2, 1), date(year, 8, 1),
                  date(year - 1, 8, 1), date(year - 1, 2, 1)]
    past = [d for d in candidates if d <= today]
    return max(past)

# ── Weekly mileage ────────────────────────────────────────────────────────────
def weekly_miles(activities: list[dict]) -> float:
    today = datetime.now(timezone.utc).date()
    start_of_week = today.toordinal() - today.weekday()  # Monday
    total = 0.0
    for a in activities:
        try:
            d = datetime.strptime(a["date"], "%Y-%m-%d").date()
            if d.toordinal() >= start_of_week:
                total += a["distance_mi"]
        except Exception:
            pass
    return round(total, 1)

# ── Coaching stats ────────────────────────────────────────────────────────────
def build_stats(activities: list[dict]) -> dict:
    from datetime import date
    today = date.today()
    season_start_date = season_start()
    start_of_week = today.toordinal() - today.weekday()

    season_acts = []
    for a in activities:
        try:
            d = datetime.strptime(a["date"], "%Y-%m-%d").date()
            if d >= season_start_date:
                season_acts.append((d, a))
        except Exception:
            pass

    # Season miles
    season_miles_total = round(sum(a["distance_mi"] for _, a in season_acts), 1)

    # Season weeks (at least 1 to avoid div-by-zero)
    if season_acts:
        earliest = min(d for d, _ in season_acts)
        season_weeks = max(1, math.ceil((today - earliest).days / 7))
    else:
        season_weeks = 1

    avg_weekly = round(season_miles_total / season_weeks, 1)

    # Longest run this season
    if season_acts:
        longest = max(season_acts, key=lambda x: x[1]["distance_mi"])
        longest_mi   = longest[1]["distance_mi"]
        longest_date = longest[1]["date"]
    else:
        longest_mi, longest_date = 0.0, ""

    # Workouts this week
    workouts_week = sum(
        1 for a in activities
        if datetime.strptime(a["date"], "%Y-%m-%d").date().toordinal() >= start_of_week
    )

    # Type breakdown (season)
    breakdown = {"easy": 0, "long": 0, "tempo": 0, "interval": 0, "race": 0}
    for _, a in season_acts:
        t = a.get("type", "easy")
        if t in breakdown:
            breakdown[t] += 1

    return {
        "season_miles":       season_miles_total,
        "season_weeks":       season_weeks,
        "avg_weekly_miles":   avg_weekly,
        "longest_run_mi":     longest_mi,
        "longest_run_date":   longest_date,
        "workouts_this_week": workouts_week,
        "workouts_total":     len(season_acts),
        "type_breakdown":     breakdown,
    }

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("Authenticating with Garmin Connect…")
    client = get_client()

    print(f"Fetching last {ACTIVITY_LIMIT} activities…")
    raw_acts = client.get_activities(0, ACTIVITY_LIMIT)

    activities = []
    for raw in raw_acts:
        parsed = parse_activity(raw, client)
        if parsed:
            activities.append(parsed)

    print(f"Parsed {len(activities)} running activities.")

    payload = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "weekly_miles": weekly_miles(activities),
        "stats":        build_stats(activities),
        "activities":   activities,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
