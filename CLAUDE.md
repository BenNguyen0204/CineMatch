# CineMatch

Flask movie recommendation app: users mark movies as watched and rate them, then get similar-movie suggestions. `README.md` covers user-facing features and setup steps.

## Session rules
- At the start of each session, read this file, `docs/PROGRESS.md` and `docs/DECISIONS.md`.
- Update `docs/PROGRESS.md` after each meaningful task. Never mark unfinished work as completed.
- Record important architectural or technical decisions in `docs/DECISIONS.md`. To change a decision, add a new entry that supersedes it; do not rewrite the old one.
- Update this file only when project-wide instructions or conventions change.
- Keep docs concise and accurate. Each fact lives in one file:
  - this file: instructions, architecture, stack, conventions
  - `PROGRESS.md`: what is done, in progress, planned or broken
  - `DECISIONS.md`: what was chosen and why

## Tech stack
Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate, PostgreSQL (Neon), pandas, scikit-learn, TMDB API, Bootstrap.

## Architecture
This is the target layout. See `docs/PROGRESS.md` for what exists today.

```
app/
  __init__.py      app factory, extension instances
  models.py        User, Movie, Watched
  tmdb.py          TMDB API client
  recommender.py   TF-IDF recommendation engine
  routes.py        web routes
  templates/
scripts/
  sync_movies.py   TMDB -> PostgreSQL pipeline
run.py             entry point (FLASK_APP)
```

Data flow: `sync_movies.py` fetches from TMDB through `tmdb.py` and stores movies in PostgreSQL. `recommender.py` reads movies and watch history. `routes.py` serves the results.

## Conventions
- Read configuration from environment variables only. Never hardcode or commit secrets, and never print `.env` values.
- `.env` holds `TMDB_API_KEY`, `DATABASE_URL` and `SECRET_KEY`.
- All TMDB calls go through `app/tmdb.py`.
- All recommendation logic lives in `app/recommender.py`, not in routes.
- Every recommendation must exclude movies in the user's `Watched` records.
- Change the database schema through Flask-Migrate migrations, not by hand.
- Do not run `flask db upgrade` or `scripts/sync_movies.py` against the Neon database without asking first.
- Before modifying files, inspect the existing code and understand its dependencies.
- Modify only files necessary for the task. Do not rewrite working code unnecessarily.
- Keep implementations simple and beginner-friendly. Avoid overengineering and unnecessary abstractions.
- After coding, run relevant tests and report what was verified. Never claim untested code works.
