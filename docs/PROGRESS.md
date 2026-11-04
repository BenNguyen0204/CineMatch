# Progress

Last updated: 2026-11-03

## Current state
The only application code is `app/__init__.py`, which has never been run. The repo also contains `README.md`, `CLAUDE.md`, `docs/`, `.env` and `gitignore`.

## Completed
- [x] Wrote `README.md` (commits `114a8f2`, `ce27b91`)
- [x] Created project docs: `CLAUDE.md`, `docs/PROGRESS.md`, `docs/DECISIONS.md` (not committed)

## Current task
- [ ] Resolve the exposed secrets (see Known issues)

## Upcoming
- [ ] Install Python and create a virtual environment
- [ ] Add `requirements.txt`
- [ ] Verify the app factory in `app/__init__.py` (written and not committed, untested until Python, `app/models.py`, `app/routes.py` and dependencies exist)
- [ ] Add `run.py`
- [ ] Add `app/models.py` with `User`, `Movie` and `Watched`, and create the first migration
- [ ] Add `app/tmdb.py`
- [ ] Add `scripts/sync_movies.py`
- [ ] Add `app/recommender.py`
- [ ] Add `app/routes.py` and `app/templates/`

The README roadmap lists post-launch ideas.

## Known issues
- **High: secrets are in the git history on GitHub.** The real `.env` was committed in `114a8f2` and pushed to `origin/main`, and is still tracked. Fix order:
  1. Rotate the Neon password and TMDB API key, and replace `SECRET_KEY`.
  2. Rename `gitignore` to `.gitignore` and stop tracking `.env`.
  3. Remove `.env` from history and force push (needs explicit approval).
- `gitignore` has no leading dot, so git ignores nothing.
- `SECRET_KEY` is only 6 characters long.
- `abc.py` is deleted locally but still tracked. The deletion is not committed.
- Python is not installed on this machine (only the Windows Store stubs), so no code can be run yet.
- The README setup steps cannot work yet: `requirements.txt`, `run.py`, migrations and `scripts/sync_movies.py` do not exist.
