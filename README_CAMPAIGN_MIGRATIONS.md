# Campaign Bot + Database Migrations

This version separates the campaign mode from the bot engine:

- `app/routes/campaign.py` handles Flask routes and saving/loading progress.
- `app/bot/` contains the bot parser, story graph, scene generator, and engine.
- `CampaignProgress` in `app/models.py` stores the user's saved campaign state.
- Flask-Migrate is enabled in `app/__init__.py`.

## Setup

```bash
python3 -m venv xenotypevenv
source xenotypevenv/bin/activate
pip install -r requirements.txt
```

## Migrations

If this repo does not already have a `migrations/` folder locally, initialize migrations once:

```bash
flask db init
```

Create and apply the migration for `CampaignProgress`:

```bash
flask db migrate -m "Add campaign progress table"
flask db upgrade
```

## Run

```bash
flask run
```

Then open:

```text
http://127.0.0.1:5000/campaign/
```

## Notes

Do not commit your virtual environment, local SQLite database, `.git/`, `__pycache__/`, or generated user-uploaded profile photos.
