from fastapi.testclient import TestClient

from app.main import app, win_percentage

client = TestClient(app)


def test_root_cheers_for_default_team():
    body = client.get("/").json()
    assert body["app"] == "windy-city-scoreboard"
    assert body["message"] == "Bear Down!"


def test_health_is_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_lists_seven_teams():
    assert len(client.get("/teams").json()) == 7


def test_get_one_team():
    body = client.get("/teams/cubs").json()
    assert body["venue"] == "Wrigley Field"
    assert body["last_title"] == 2016


def test_unknown_team_is_404():
    assert client.get("/teams/packers").status_code == 404


def test_win_percentage():
    assert win_percentage(3, 1) == 0.75


def test_win_percentage_no_games():
    assert win_percentage(0, 0) == 0.0
