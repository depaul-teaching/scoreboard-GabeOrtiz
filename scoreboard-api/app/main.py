"""Windy City Scoreboard: the IT 390 class app.

A small API about Chicago's pro teams. We containerize it, ship it with
GitHub Actions, and run it on Kubernetes, one week at a time.
"""
import os
import sys

from fastapi import FastAPI, HTTPException

from app.teams import TEAMS

# Set by the pipeline at build time (see the Dockerfile ARG/ENV).
BUILD_SHA = os.getenv("BUILD_SHA", "local-dev")

# Pick your team with an environment variable. Default: Bears.
FAVORITE_TEAM = os.getenv("FAVORITE_TEAM", "bears").lower()

if FAVORITE_TEAM not in TEAMS:
    # Fail fast and loudly: a bad config should stop the app at startup,
    # not show up later as a confusing error.
    sys.exit(
        f"FAVORITE_TEAM={FAVORITE_TEAM!r} is not a Chicago team. "
        f"Pick one of: {', '.join(sorted(TEAMS))}"
    )

app = FastAPI(title="Windy City Scoreboard")


def win_percentage(wins: int, losses: int) -> float:
    """Share of games won, rounded to 3 places like a standings page."""
    games = wins + losses
    if games == 0:
        return 0.0
    return round(wins / games, 3)


@app.get("/")
def root():
    team = TEAMS[FAVORITE_TEAM]
    return {
        "app": "windy-city-scoreboard",
        "favorite_team": team["name"],
        "message": team["cheer"],
        "build": BUILD_SHA,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/teams")
def list_teams():
    return [{"slug": slug, **team} for slug, team in TEAMS.items()]


@app.get("/teams/{slug}")
def get_team(slug: str):
    team = TEAMS.get(slug.lower())
    if team is None:
        raise HTTPException(status_code=404, detail=f"No Chicago team called {slug!r}")
    return {"slug": slug.lower(), **team}


@app.get("/record")
def record(wins: int, losses: int):
    return {"wins": wins, "losses": losses, "pct": win_percentage(wins, losses)}
