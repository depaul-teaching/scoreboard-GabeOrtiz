# Windy City Scoreboard

The IT 390 class app: a small API about Chicago's pro teams. This is only the starting code. In class we turn it into a repo, a container, a pipeline, and a pod, one step at a time.

## Run it locally

With Python 3.12:

```bash
cd scoreboard-api
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -v
uvicorn app.main:app --reload
```

Then open http://localhost:8000 or http://localhost:8000/docs.

## The API

| Endpoint | Returns |
|---|---|
| `GET /` | Your favorite team's cheer, plus the build you are running |
| `GET /health` | `{"status": "ok"}` |
| `GET /teams` | All seven Chicago pro teams |
| `GET /teams/{slug}` | One team, e.g. `/teams/bulls`. Unknown teams return 404. |
| `GET /record?wins=10&losses=7` | Win percentage, standings style |

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `FAVORITE_TEAM` | `bears` | One of `bears`, `bulls`, `cubs`, `white-sox`, `blackhawks`, `sky`, `fire`. Anything else stops the app at startup, on purpose. |
| `BUILD_SHA` | `local-dev` | The commit the image was built from. The pipeline sets it. |
